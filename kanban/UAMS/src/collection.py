"""
取得所有使用者ID
用在"加入使用者至專案"功能
"""
from typing import List


class GlobalUser:
    def __init__(self, Firebase):
        self.firebase = Firebase
        self.database = self.firebase.firestore()
        self.user_info_db = self.database.collection('users')

    def get_all_id(self):
        docs = self.user_info_db.get()
        user_id_list = list()
        for doc in docs:
            user_id_list.append(doc.id)
        return user_id_list  # type: List[str]

    def get_all_email(self):
        docs = self.user_info_db.get()
        user_email_list = list()
        for doc in docs:
            user_email_list.append(doc.to_dict()['email'])
        return user_email_list  # type: List[str]