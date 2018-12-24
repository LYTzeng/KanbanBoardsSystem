"""專案管理子系統
建立專案、查詢專案成員、權限、專案Metadata、任務移動/增加/刪除 等
"""
from typing import (List, Dict)


class Project:
    def __init__(self, Firebase):
        """初始化
        :param Firebase: Firebase 的 API 認證 Class
        """
        self.firebase = Firebase
        self.database = self.firebase.firestore()  # Firestore
        self.project_collection = self.database.collection('projects')

        self.project_document = None
        self.project_id = None
        self.name = None
        self.owner = None
        self.members = None
        self.columns = {'todo': list(), 'progress': list(), 'done': list()}
        self.attr = ['todo', 'progress', 'done']

    def create(self, request):
        """建立全新專案"""
        self.name = request.POST.get('name')
        self.owner = request.POST.get('owner')
        try:
            self.members = self._member_parser(request.POST.get('members'))  # type: List[str]
        finally:  # 一開始建立專案可以不加入其他人
            pass

        project_data = {
            'name': self.name,  # type: str
            'owner': self.owner,  # type: str
            'members': self.members,  # type: List[str]
            'columns': self.columns,  # type: Dict[str: List[str]]
            'attr': self.attr  # type: List[str]
        }
        ref = self.project_collection.document()
        self.project_id = ref.id
        ref.set(project_data)
        self.get_board(project_id=ref.id)
        self._add_project_to_user_doc()

    def add_members(self, request):
        """在舊專案新增成員"""
        members_to_add = request.POST.get('members-to-add')  # type: str
        self.members.extend(self._member_parser(members_to_add))  # type: List[str]
        self.project_document.update(
            {'members': self.members}
        )
        self._add_project_to_user_doc()

    def delete_member(self, request):
        """在舊專案移除成員"""
        member_to_del = request.POST.get('member-to-delete')  # type: str
        try:
            self.members.remove(member_to_del)
        except ValueError:
            return "The member has been kicked out!"
        self.project_document.update(
            {'members': self.members}
        )

    def rename(self, request):
        """重新命名專案"""
        new_name = request.POST.get('new-name')
        self.project_document.update(
            {'name': new_name}
        )

    def get_board(self, request=None, project_id: str = str()):
        """開啟舊專案"""
        if request is not None:
            self.project_id = request.POST.get('project-id')
        elif project_id != str():
            self.project_id = project_id
        else:
            raise ValueError
        self.project_document = self.project_collection.document(self.project_id)
        project_data = self.project_document.get().to_dict()
        self.name = project_data['name']
        self.owner = project_data['owner']
        self.members = project_data['members']
        self.columns = project_data['columns']
        self.attr = project_data['attr']
        return project_data  # type: dict

    def move_task(self, task_id: str, src: str, dst: str):
        """
        在看板上移動任務
        :param task_id:
        :param src:
        :param dst:
        :return:
        """
        # TODO: 整合jqwidget API的動作
        if src and dst not in self.attr:
            raise ValueError
        self.columns[src].remove(task_id)
        self.columns[dst].append(task_id)
        self.project_document.update({'columns': self.columns})

    def add_task(self, task_id: str, column_to_add_to: str):
        if column_to_add_to not in self.attr:
            raise ValueError
        self.columns[column_to_add_to].append(task_id)
        self.project_document.update({'columns': self.columns})

    def del_task(self, task_id: str, column_to_delete_from: str):
        if column_to_delete_from not in self.attr:
            raise ValueError
        self.columns[column_to_delete_from].remove(task_id)
        self.project_document.update({'columns': self.columns})

    def delete_project(self):
        self.project_document.delete()
        self.__init__(self.firebase)

    def _member_parser(self, members_str):
        result = [x.strip() for x in members_str.split(',')]
        return result  # type: List[str]

    def _add_project_to_user_doc(self):
        for member in self.members:
            project_list = self.database.collection('users').document(member).get().to_dict()['project_list']
            project_list.append(self.project_id)
            self.database.collection('users').document(member).update({'project_list': project_list})

    def get_proj_name_by_id_dict(self, project_ids: list):
        if project_ids is None:
            return None
        names = list()
        for id in project_ids:
            data = self.project_collection.document(id).get().to_dict()
            names.append({"id": id, "name": data['name']})
        return names  # type: dict

    def get_project_task_ids(self):
        task_ids = self.project_document.collection("tasks").get()
        task_id_list = list()        
        for id in task_ids:
            task_id_list.append(id.id)
        return task_id_list
