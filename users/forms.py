from django import forms
from django.forms.util import ErrorList

class DivErrorList(ErrorList):
     def __unicode__(self):
         return self.as_divs()
     def as_divs(self):
         if not self: return u''
         return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'text'}))
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'text'}))

class LoginForm(forms.Form):
    pass
