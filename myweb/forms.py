from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']
class RegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password','email']