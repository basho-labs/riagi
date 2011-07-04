from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('images/index.html', {"name": request.GET.get("name")})
