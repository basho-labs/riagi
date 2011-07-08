from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class LoginForm(forms.Form):
    pass
