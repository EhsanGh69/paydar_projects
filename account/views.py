from django.shortcuts import render
from django.contrib.auth.views import LoginView



class CustomLogin(LoginView):
    redirect_authenticated_user = True
