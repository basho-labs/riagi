from django.http import HttpResponse
from django.shortcuts import render
from users.service import UsersRiakService

def home(request):
    user = None
    if 'username' in request.session:
        user_service = UsersRiakService()
        user = user_service.get(request.session['username'])

    return render(request, 'home.html', {"user": user})
