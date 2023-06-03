from django.shortcuts import render
from django.contrib.auth.views import LoginView

from .forms import AuthenticateForm



class CustomLogin(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticateForm

