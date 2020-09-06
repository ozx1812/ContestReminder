from django.shortcuts import render, HttpResponse
from .settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import requests
import schedule
import time
from .schd import Reminder
from users.models import CustomUser,Profile
from .views import Reminder


def home(request):

    return render(request,'home.html')

def testing(request):
    users = CustomUser.objects.all()
    rem = Reminder()
    rem.reminder(users)
    return HttpResponse('testing...')


def my_profile(request):
    pass

def profile_update(request):
    pass

def signup_login(request):
    pass


