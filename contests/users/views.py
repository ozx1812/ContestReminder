from django.shortcuts import render
from .models import Profile,CustomUser
from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (CustomUserCreationForm,CustomUserChangeForm)
from django.contrib.auth.decorators import login_required
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('myprofile')
    template_name = 'signup.html'

class SignInView(LoginView):
    template_name = 'signin.html'
    authentication_form = AuthenticationForm
    form_class = AuthenticationForm
    success_url = reverse_lazy('myprofile')


class LogOutView(LoginRequiredMixin,LogoutView):
    template_name = 'signin.html'
    success_url = reverse_lazy('signin')


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    fields = ['name', 'codeChef', 'codeForces', 'hackerEarth', 'hackerRank', 'spoj']
    template_name = 'profileupdate.html'
    success_url = reverse_lazy('myprofile')
    

    def get_object(self):
        return self.request.user.profile


class MyProfileView(LoginRequiredMixin,DetailView):
    template_name = 'myprofile.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile



