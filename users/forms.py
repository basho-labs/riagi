import re

from django import forms
from django.forms.util import ErrorList

from users.service import UserService

class DivErrorList(ErrorList):
     def __unicode__(self):
         return self.as_divs()
     def as_divs(self):
         if not self: return u''
         return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'text'}))
    username = forms.RegexField(regex=r'^\w+$', max_length=20, widget=forms.TextInput(attrs={'class':'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'text'}))

    def save(self):
        user_data = self.cleaned_data
        user_service = UserService()
        return user_service.save(user_data)

class LoginForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=20, widget=forms.TextInput(attrs={'class':'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'text'}))

    def logged_in(self):
        user_service = UserService()
        user = user_service.login(self.cleaned_data['username'], self.cleaned_data['password'])
        if user:
            self.cleaned_data['user_id'] = user.get_key()
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Invalid username or password')
