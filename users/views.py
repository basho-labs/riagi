from django.http import HttpResponse
from django.shortcuts import render_to_response
from users.forms import SignupForm
from django.template import RequestContext
from users.forms import DivErrorList

def signup(request):
    signup_form = SignupForm(request.POST, label_suffix="<br/>", error_class=DivErrorList)
    if request.method == "POST":
        if signup_form.is_valid():
            signup_form.save()
    else:
        pass
    
    return render_to_response('users/signup.html', {'signup_form': signup_form},
            context_instance=RequestContext(request))
