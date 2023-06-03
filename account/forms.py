from django import forms
from django.contrib.auth.forms import AuthenticationForm




class AuthenticateForm(AuthenticationForm):
    use_required_attribute = False


