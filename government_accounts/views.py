from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from .models import Receive
from .forms import ReceiveForm



class ReceiveList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"


class ReceiveCreate(LoginRequiredMixin, CreateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")

