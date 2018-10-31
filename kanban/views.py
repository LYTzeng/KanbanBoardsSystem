from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext

#kevin
class KBboard(View):

    def get(self, request):
        return render(request, "board.html")


class KBsettings(View):

    def get(self, request):
        return render(request, "settings.html")