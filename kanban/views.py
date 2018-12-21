import sys
from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext
from django.http import JsonResponse, HttpResponseRedirect
from kanban.UAMS.src.user import User
from kanban.PMS.src.project import Project
from kanban.TMS.src.task import Task
from kanban.firebase.setup import Firebase, Pyrebase


RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production
firebase = Firebase(RUNNING_DEVSERVER)
pyrebase = Pyrebase()
user = User(firebase, pyrebase)


class KanbanBoard(View):
    def get(self, request):
        return render(request, "board.html")


class KanbanSettings(View):
    def get(self, request):
        return render(request, "settings.html")


class KanbanProjData(View):
    def get(self, request):
        response = JsonResponse({"json": "response"})
        return response


class Index(View):
    def get(self, request):
        return render(request, "index.html")


class Login(View):
    """登入"""
    def post(self, request):
        result = user.login(request)
        if type(result) == str:
            return render(request, "index.html", {"message": result})
        else:
            return render(result, "board.html")


class SignUp(View):
    """註冊"""
    def post(self, request):
        result = user.create(request)
        if type(result) == str:
            return render(request, "index.html", {"message": result})
        else:
            return render(result, "board.html")


class SignOut(View):
    """登出"""
    def get(self, request):
        user.sign_out(request)
        return HttpResponseRedirect('/')
