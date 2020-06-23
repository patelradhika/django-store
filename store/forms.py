from django import forms
from django.contrib.auth.models import User

from .models import UserImage


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    checkpwd = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AccountForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    checkpwd = forms.CharField(widget=forms.PasswordInput(), required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = UserImage
        fields = ['profile_pic',]