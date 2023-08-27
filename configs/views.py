from django.shortcuts import render
from django.contrib.auth.decorators import login_required





@login_required
def index(request):

    return render(request, 'home.html', {})


def csrf_failure(request, reason=""):
    return render(request, '403.html', {})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request, exception=None):
    return render(request, '500.html', {})


