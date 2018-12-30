"""KB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import sys
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from kanban import views


RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production

urlpatterns = [
    # Index
    url(r'^$', views.Index.as_view()),
    url(r'^index/(\d+)/$', views.Index.as_view()),
    # Kanban Board Page
    url(r'^board/$', views.KanbanBoard.as_view()),
    url(r'^KanbanProjJSON/$', views.KanbanProjJSON.as_view()),
    # UAMS
    url(r'^login/$', views.Login.as_view()),
    url(r'^signup/', views.SignUp.as_view()),
    url(r'^signout/$', views.SignOut.as_view()),
    # PMS & TMS
    url(r'^board/create/$', views.CreateProject.as_view()),
    url(r'^board/movetask/$', views.MoveTask.as_view()),
    url(r"^board/addTask/$", views.AddTask.as_view()),
    url(r'^board/deleteTask/$', views.DeleteTask.as_view()),
    url(r'^board/deleteMember/$', views.DeleteMember.as_view()),
    url(r'^board/addMember/$', views.AddMember.as_view()),
    url(r'^board/deleteProject/$', views.DeleteProject.as_view()),
]

if not RUNNING_DEVSERVER:
    urlpatterns  += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
