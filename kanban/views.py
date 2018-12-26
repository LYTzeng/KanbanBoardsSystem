import sys
from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
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


class Index(View):
    def get(self, request):
        return render(request, "index.html")


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
        if 'projNum' not in request.GET:
            # 開啟第一個專案
            if project_name_id_dict != [] : proj_data = project.get_board(project_id=project_list[0])
            current_project_id = project_list[0]
        else:
            proj_number = int(request.GET.get('projNum'))
            proj_data = dict()
            if project_name_id_dict != []: proj_data = project.get_board(project_id=project_list[proj_number])
            current_project_id = project_list[proj_number]
        # 補充前端必要參數
        username = user.username
        is_manager = project.is_manager(username)
        proj_members = project.members
        proj_name = project.name
        return render(request, "board.html", locals())


class KanbanSettings(View):
    def get(self, request):
        return render(request, "settings.html")


class KanbanProjJSON(View):
    def get(self, request):
        data = project.get_board(project_id=project.project_id)
        return JsonResponse(data)


'''
    PMS View
'''


class CreateProject(View):
    """建立專案"""
    def post(self, request):
        project.create(request)
        print(project.name, project.owner, project.members)
        return HttpResponseRedirect("/board/")


class GetAllProjMembers(View):
    """取得專案所有成員"""
    def get(self, request):
        members_list = project.members
        return JsonResponse(members_list, safe=False)


class DeleteMember(View):
    """從專案移除成員"""
    def post(self, request):
        project.delete_member(request)
        return HttpResponse("OK")


class DeleteProject(View):
    def post(self, request):
        project.delete_project()
        return HttpResponse("OK")


'''
    TMS View
'''


class MoveTask(View):
    """移動卡片"""
    def post(self, request):
        task_id = request.POST.get('taskId')
        source = request.POST.get('src')
        destination = request.POST.get('dst')
        project.move_task(task_id, source, destination)
        return HttpResponse("OK")


class AddTask(View):
    """新增卡片"""
    # def __init__(self):
    #     super(AddTask, self).__init__()
    #     self.

    def post(self, request):
        task = Task(firebase, project.project_id)
        task.add_task(request)
        project.add_task(task.task_id, request.POST.get('column'))
        return JsonResponse({"task_id": task.task_id})




class DeleteTask(View):
    """刪除卡片"""
    def post(self, request):
        project.del_task(request.POST.get('taskId'), request.POST.get('column'))
        task = Task(firebase, project.project_id)
        task.get(request)
        task.del_task()
        return HttpResponse("OK")

'''
    UAMS View
'''


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
