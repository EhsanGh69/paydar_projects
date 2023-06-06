from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .models import Receive, Organization
from .forms import ReceiveCreateForm, ReceiveUpdateForm, OrganizationForm


# Receive - Start

class ReceiveList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9


class ReceiveCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveCreateForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ثبت گردید"
    

class ReceiveUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveUpdateForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ویرایش شد"


class ReceiveDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Receive
    template_name = 'government_accounts/confirm_delete.html'
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت حذف شد"


class ReceiveSearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        if query is not None:
            search = Receive.objects.search(query)
            if search:
                return search
            else:
                not_found = True
        
        return Receive.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        return context

# Receive - End

# ---------------------------------------

# Organization - Start

class OrganizationList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/organization_list.html'
    model = Organization
    context_object_name = "organizations"


class OrganizationCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Organization
    template_name = 'government_accounts/organization_create_update.html'
    form_class = OrganizationForm
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت افزوده شد"
    

class OrganizationUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Organization
    template_name = 'government_accounts/organization_create_update.html'
    form_class = OrganizationForm
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت ویرایش شد"


class OrganizationDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Organization
    template_name = 'government_accounts/confirm_delete.html'
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت حذف شد"


# Organization - End


# ---------------------------------------------

