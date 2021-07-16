from django.shortcuts import render
from . import models
# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def registrationPage(request):
    return render(request, 'pages/registration.html')


def loginPage(request):

    constant = {
        "title": "This is login page",
    }

    return render(request, 'pages/login.html', constant)


def logoutPage(request):
    
    return render(request, 'pages/index.html')
