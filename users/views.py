from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from users.forms import SignupForm
from django.template import RequestContext
from users.forms import DivErrorList

def signup(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        signup_form = SignupForm(request.POST, label_suffix="<br/>", error_class=DivErrorList)
        if signup_form.is_valid():
            request.session['user_id'] = signup_form.save()
            return HttpResponseRedirect("/")
    else:
        signup_form = SignupForm(label_suffix="<br/>") 
    
    return render_to_response('users/signup.html', {'signup_form': signup_form},
            context_instance=RequestContext(request))
