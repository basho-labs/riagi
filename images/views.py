from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from images.forms import UploadForm

def upload(request):
    if request.method == "POST":
       upload = UploadForm(request.POST, request.FILES)
       upload.save(request)

    return HttpResponseRedirect("/")
