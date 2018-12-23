import sys
from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseRedirect
from kanban.UAMS.src.user import User
from kanban.UAMS.src.collection import GlobalUser
from kanban.PMS.src.project import Project
from kanban.TMS.src.task import Task
from kanban.firebase.setup import Firebase, Pyrebase
from typing import List, Dict


RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production
firebase = Firebase(RUNNING_DEVSERVER)
pyrebase = Pyrebase()
user = User(firebase, pyrebase)     # 使用者物件
global_user = GlobalUser(firebase)  # 全體使用者
project = Project(firebase)  # 專案物件


class KanbanBoard(View):
    def get(self, request):
        # 驗證登入是否過期
        if 'idToken' not in request.session:
            return HttpResponseRedirect("/")
        # 刷新使用者狀態
        user.refresh()
        # 屬於user的專案列表
        project_name_id_dict = project.get_proj_name_by_id_dict(user.project_list)  # type: Dict[str, str]
        project_list = user.project_list  # type: List[str] # project id
        # 開啟第一個專案
        if project_name_id_dict != [] : proj_data = project.get_board(project_id=project_list[0])
        return render(request, "board.html", locals())


class KanbanSettings(View):
    def get(self, request):
        return render(request, "settings.html")


class KanbanProjJSON(View):
    def get(self, request):
        data = project.get_board(project_id=project.project_id)
        return JsonResponse(data)


class Index(View):
    def get(self, request):
        return render(request, "index.html")


class CreateProject(View):
    """建立專案"""
    def post(self, request):
        project.create(request)
        print(project.name, project.owner, project.members)
        return HttpResponseRedirect("/board/")


class Login(View):
    """登入"""
    def post(self, request):
        result = user.login(request)
        if type(result) == str:
            return render(request, "index.html", {"message": result})
        else:
            return HttpResponseRedirect("/board/")


class SignUp(View):
    """註冊"""
    def post(self, request):
        result = user.create(request)
        if type(result) == str:
            return render(request, "index.html", {"message": result})
        else:
            return HttpResponseRedirect("/board/")


class SignOut(View):
    """登出"""
    def get(self, request):
        user.sign_out(request)
        return HttpResponseRedirect('/')


class AllUserJSON(View):
    """取得所有使用者ID的JSON"""
    def get(self, request):
        # 全體使用者ID清單
        all_user_id = global_user.get_all_id()  # type: List[str]
        json = list()
        for user_id in all_user_id:
            json.append(user_id)
        return JsonResponse(json, safe=False)  # type: List[str]
