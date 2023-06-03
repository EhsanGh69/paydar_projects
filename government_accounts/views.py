from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .models import Receive
from .forms import ReceiveCreateForm, ReceiveUpdateForm




class ReceiveList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"


class ReceiveCreate(LoginRequiredMixin, CreateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveCreateForm
    success_url = reverse_lazy("government_accounts:receives")


class ReceiveUpdate(LoginRequiredMixin, UpdateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveUpdateForm
    success_url = reverse_lazy("government_accounts:receives")


class ReceiveDelete(LoginRequiredMixin, DeleteView):
    model = Receive
    template_name = 'government_accounts/confirm_delete.html'
    success_url = reverse_lazy("government_accounts:receives")



