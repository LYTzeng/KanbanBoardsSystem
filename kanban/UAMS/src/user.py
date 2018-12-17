"""帳戶管理子系統
這裡是帳戶管理的User物件
注意：呼叫function都要從View傳入request參數
註冊: User.create()
登入: User.login()
登出: User.sign_out()
登入有效性及權限驗證: User.authorize()
"""
import requests
import json


class User():

    def __init__(self, Firebase, Pyrebase):
        """初始化
        :param Credentials: Firebase 的 API 認證 Class
        """
        self.firebase = Firebase
        self.database = self.firebase.firestore()
        self.user_info_db = self.database.collection('users')
        self.authentication = Pyrebase.auth()

        self.user = None  # Firebase user 已註冊或登入的使用者
        self.email = None
        self.name = None
        self.username = None

    def create(self, request):
        """註冊"""
        self.username = request.POST.get('username')  # 帳號 注意是唯一的!
        self.name = request.POST.get('name')        # User名稱
        self.email = request.POST.get('email')      # 信箱
        meema = request.POST.get('meema')      # 密碼
        if self._email_exists or self._username_exists:
            return "email或帳號已註冊"
        else:
            # 密碼資訊寫到Firebase Auth
            self.user = self.authentication.create_user_with_email_and_password(self.email, meema)
            # 一般資訊寫到Firestore
            user_data = {
                'uid': self.user['localId'],
                'type': 'normal',
                'name': self.name,
                'email': self.email,
            }
            self.user_info_db.document(self.username).set(user_data)
        return self.login(request)

    def login(self, request):
        """登入"""
        self.email = request.POST.get('email')
        meema = request.POST.get('meema')
        try:
            self.user = self.authentication.sign_in_with_email_and_password(self.email, meema)  # 從 Firebase Auth 驗證
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            message = error['message']
            return message + ": " + self.email  # 登入失敗 回傳錯誤訊息
        if self.user['registered']:
            request.session['idToken'] = self.user['idToken']  # token有時效性
            request.session['localId'] = self.user['localId']  # 唯一的User ID
            request.session['username'] = self._get_username_by_email()
            request.session.set_expiry(1800)
            return request
        else:
            message = "Unknown Error"
            return message

    def authorize(self, idToken, localId):
        """驗證使用者，未登入者限制權限"""
        current_user = self.authentication.current_user
        localId_real = current_user['localId']
        localId_session = localId
        token_real = current_user['idToken']
        token_session = idToken
        EXPIRED = False
        try:
            self.authentication.get_account_info(token_session)
        except Exception:
            EXPIRED = True
        if not EXPIRED and localId_real == localId_session and token_real == token_session:
            self.authentication.refresh(current_user['refreshToken'])
            return True
        else:
            return False

    def delete_user(self, request):
        """刪除帳號"""
        user = self.login(request)
        if self._email_exists:
            try:
                # auth.delete_user(user.session['localId'])
                self.firebase.auth().delete_user(user.session['localId'])
            except:
                print(user)
            self.user_info_db.document(self._get_username_by_email()).delete()

    def sign_out(self, request):
        """登出"""
        try:
            # 清除 Session
            del request.session['idToken']
            del request.session['localId']
            del request.session['username']
            return request
        except Exception as e:
            raise e

    @property
    def _email_exists(self):
        """確認該信箱是否已經註冊
        :param email:
        :return: Boolean: True>exists
        """
        user = self._query_user_by_email()
        return user != {}

    @property
    def _username_exists(self):
        """確認帳號使否已被註冊
        :param username:
        :return: Boolean: True>exists
        """
        query = self.database.collection('users').document(self.username).get()
        user = query.to_dict()
        return user is not None

    def _get_username_by_email(self):
        query = self.database.collection('users').where('email', '==', self.email).get()
        username = str()
        for q in query:
            username = q.id
        return username

    def _query_user_by_email(self):
        query = self.database.collection('users').where('email', '==', self.email).get()
        user = dict()
        for q in query:
            user = q.to_dict()
        return user
