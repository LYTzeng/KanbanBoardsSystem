"""帳戶管理子系統
這裡是帳戶管理的User物件
注意：呼叫function都要從View傳入request參數
註冊: User.create()
登入: User.login()
登出: User.logout()
登入有效性及權限驗證: User.authorize()
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase
import requests
import json
from ..src import FirebaseAPIKey


class User():

    def __init__(self, DEVSERVER = True):
        """初始化
        :param DEVSERVER: 是否運行於開發環境?
        """
        self.DEVSERVER = DEVSERVER
        if DEVSERVER:  # 本地開發環境 初始化Firebase
            self._cred = credentials.Certificate('D:/NTUT/軟體工程/project/kanban-board-sys-firebase-adminsdk.json')
            firebase_admin.initialize_app(self._cred)
        else:          # Google平台 初始化Firebase
            self._cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(self._cred, {
                'projectId': 'kanban-board-sys',
            })
        self.database = firestore.client()  # Firestore
        self.user_info_db = self.database.collection('users')
        self._conf = FirebaseAPIKey.get()
        self.authentication = pyrebase.initialize_app(self._conf).auth()  # Firebase Auth

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
        if not self._email_exists or not self._username_exists:
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
            return message  # 登入失敗 回傳錯誤訊息
        if self.user['registered']:
            request.session['idToken'] = self.user['idToken']  # token有時效性
            request.session['localId'] = self.user['localId']  # 唯一的User ID
            request.session['username'] = self._get_username_by_email()
            request.session.set_expiry(1800)
            return request
        else:
            message = "Unknown Error"
            return message

    def authorize(self):
        return NotImplemented

    @property
    def _email_exists(self):
        """確認該信箱是否已經註冊
        :param email:
        :return: True>exists
        """
        user = None
        user = self._query_user_by_email()
        return user is not None

    @property
    def _username_exists(self):
        """確認帳號使否已被註冊
        :param username:
        :return: True>exists
        """
        user = None
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
