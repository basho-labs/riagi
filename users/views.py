from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from users.forms import SignupForm, LoginForm
from users.forms import DivErrorList


def signup(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        signup_form = SignupForm(request.POST,
                                 label_suffix="<br/>",
                                 error_class=DivErrorList)
        if signup_form.is_valid():
            request.session['user_id'] = signup_form.save()
            return HttpResponseRedirect("/")
    else:
        signup_form = SignupForm()

    return render_to_response('users/signup.html',
                              {'signup_form': signup_form},
                              context_instance=RequestContext(request))


def logout(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            del request.session['user_id']

    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user_id'] = form.cleaned_data['user_id']
            return redirect('/')
        else:
            return render_to_response('users/login.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = LoginForm(label_suffix="<br/>")
        return render_to_response('users/login.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
