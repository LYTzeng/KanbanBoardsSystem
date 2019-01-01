import sys
from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from kanban.UAMS.src.user import User
from kanban.UAMS.src.collection import GlobalUser
from kanban.PMS.src.project import Project, ProjectReader
from kanban.TMS.src.task import Task
from kanban.firebase.setup import Firebase, Pyrebase
from typing import List, Dict


RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production
firebase = Firebase(RUNNING_DEVSERVER)
pyrebase = Pyrebase()
user = dict()  # 使用者物件字典
global_user = GlobalUser(firebase)  # 全體使用者
project = dict()  # 專案物件字典
proj_reader = ProjectReader(firebase)


class Index(View):
    def get(self, request):
        allUserId = global_user.get_all_id()
        allUserEmail = global_user.get_all_email()
        return render(request, "index.html", locals())


class KanbanBoard(View):
    def get(self, request):
        # 驗證登入是否過期
        if 'idToken' not in request.session:
            return HttpResponseRedirect("/")
        # 刷新使用者狀態
        try:
            user[request.session['email']].refresh()
        except Exception:
            user[request.session['email']] = User(firebase, pyrebase)
            print("KanbanBoard.get user.refresh exception")
        # 屬於user的專案列表
        project_name_id_dict = proj_reader.get_proj_name_by_id_dict(user[request.session['email']].project_list)  # type: Dict[str, str]
        project_list = user[request.session['email']].project_list  # type: List[str] # project id
        # 給前端使用參數
        username = user[request.session['email']].username
        name = user[request.session['email']].name
        email = user[request.session['email']].email
        localId = user[request.session['email']].localId
        # 給名下無專案的用戶
        if project_list == []:
            proj_members = []
            all_user_id = global_user.get_all_id()
            return render(request, "board.html", locals())
        # 給剛登入的狀態
        elif 'projNum' not in request.GET:
            # 開啟第一個專案
            project[project_list[0]] = Project(firebase)
            request.session['current_project'] = project_list[0]
            if project_name_id_dict != [] : proj_data = project[project_list[0]].get_board(project_id=project_list[0])
            current_project_id = project_list[0]
        # 已經查看過2個以上專案之用戶
        else:
            proj_number = int(request.GET.get('projNum'))
            project[project_list[proj_number]] = Project(firebase)
            request.session['current_project'] = project_list[proj_number]
            proj_data = dict()
            if project_name_id_dict != []: proj_data = project[request.session['current_project']].get_board(project_id=project_list[proj_number])
            current_project_id = project_list[proj_number]
        # 補充前端必要參數
        is_owner = project[request.session['current_project']].is_manager(username)
        owner = project[request.session['current_project']].owner
        proj_members = project[request.session['current_project']].members
        proj_name = project[request.session['current_project']].name
        all_user_id = global_user.get_all_id()
        return render(request, "board.html", locals())


class KanbanProjJSON(View):
    def get(self, request):
        data = project[request.session['current_project']].get_board(project_id=project[request.session['current_project']].project_id)
        return JsonResponse(data)


'''
    PMS View
'''


class CreateProject(View):
    """建立專案"""
    def post(self, request):
        new_project = Project(firebase)
        new_proj_id = new_project.create(request)
        request.session['current_project'] = new_proj_id
        project[request.session['current_project']] = new_project
        return HttpResponseRedirect("/board/")


class DeleteMember(View):
    """從專案移除成員"""
    def post(self, request):
        project[request.session['current_project']].delete_member(request)
        return HttpResponse("OK")


class AddMember(View):
    """新增成員"""
    def post(self, request):
        project[request.session['current_project']].add_member(request)
        return HttpResponse("OK")


class DeleteProject(View):
    def get(self, request):
        project[request.session['current_project']].delete_project()
        del project[request.session['current_project']]
        return HttpResponseRedirect("/board/")


'''
    TMS View
'''


class MoveTask(View):
    """移動卡片"""
    def post(self, request):
        task_id = request.POST.get('taskId')
        source = request.POST.get('src')
        destination = request.POST.get('dst')
        project[request.session['current_project']].move_task(task_id, source, destination)
        return HttpResponse("OK")


class AddTask(View):
    """新增卡片"""
    def post(self, request):
        task = Task(firebase, request.session['current_project'])
        task.add_task(request)
        project[request.session['current_project']].add_task(task.task_id, request.POST.get('column'))
        return JsonResponse({"task_id": task.task_id})


class DeleteTask(View):
    """刪除卡片"""
    def post(self, request):
        project[request.session['current_project']].del_task(request.POST.get('taskId'), request.POST.get('column'))
        task = Task(firebase, request.session['current_project'])
        task.get(request)
        task.del_task()
        return HttpResponse("OK")


'''
    UAMS View
'''


class Login(View):
    """登入"""
    def post(self, request):
        user[request.POST.get('email')] = User(firebase, pyrebase)
        result = user[request.POST.get('email')].login(request)
        if type(result) == str:
            print(result)
            return render(request, "index.html", {"message": result})
        else:
            return HttpResponseRedirect("/board/")


class SignUp(View):
    """註冊"""
    def post(self, request):
        user[request.POST.get('email')] = User(firebase, pyrebase)
        result = user[request.POST.get('email')].create(request)
        if type(result) == str:
            return render(request, "index.html", {"message": result})
        else:
            return HttpResponseRedirect("/board/")


class SignOut(View):
    """登出"""
    def get(self, request):
        try:
            user[request.session['email']].sign_out(request)
            del user[request.session['email']]
        except KeyError:
            pass
        return HttpResponseRedirect('/')


class Rename(View):
    """改名字"""
    def post(self, request):
        user[request.session['email']].rename(request)
        return HttpResponse("OK")