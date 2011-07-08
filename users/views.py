from django.http import HttpResponse
from django.shortcuts import render_to_response
from users.forms import SignupForm

def signup(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
    else:
        signup_form = SignupForm()
    
    return render_to_response('users/signup.html', {'signup_form': signup_form})
