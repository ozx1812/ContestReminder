from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django import forms
from .models import (CustomUser, Profile)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(widget=forms.PasswordInput)

