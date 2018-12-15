import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


class Firebase():
    def __init__(self, DEVSERVER = True):
        self.DEVSERVER = DEVSERVER
        if DEVSERVER:  # 本地開發環境 初始化Firebase
            self._cred = credentials.Certificate('D:/NTUT/軟體工程/project/kanban-board-sys-firebase-adminsdk.json')
            firebase_admin.initialize_app(self._cred)
        else:  # Google平台 初始化Firebase
            self._cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(self._cred, {
                'projectId': 'kanban-board-sys',
            })

    def firestore(self):
        return firestore.client()

    def auth(self):
        return auth