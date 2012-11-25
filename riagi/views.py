from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext

from riagi.users.service import UserService
from riagi.images.forms import UploadForm


def home(request):
    user = None
    if 'user_id' in request.session:
        user_service = UserService()
        user = user_service.get(request.session['user_id'])

    upload_form = UploadForm(label_suffix="<br/>")

    return render(request, 'home.html',
                  {"user": user, "upload_form": upload_form},
                  context_instance=RequestContext(request))
