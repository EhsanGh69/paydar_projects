from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView



from .models import Receive, Organization, Payment, Activity
from .forms import (
    ReceiveCreateForm, 
    ReceiveUpdateForm, 
    OrganizationForm,
    PaymentCreateForm,
    PaymentUpdateForm,
    ActivityCreateForm,
    ActivityUpdateForm
)

# Receive - Start

class ReceiveList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:receives_search'
        return context


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
        context['search_url'] = 'government_accounts:receives_search'
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

# Payment - Start


class PaymentList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:payments_search'
        return context


class PaymentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentCreateForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ثبت گردید"


class PaymentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentUpdateForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ویرایش شد"


class PaymentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Payment
    template_name = 'government_accounts/confirm_delete.html'
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت حذف شد"


class PaymentSearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        if query is not None:
            search = Payment.objects.search(query)
            if search:
                return search
            else:
                not_found = True
        
        return Payment.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:payments_search'
        return context

# Payment - End

# ---------------------------------------------

# Activity - Start

class ActivityList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/activity_list.html'
    model = Activity
    context_object_name = "activities"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:activities_search'
        return context


class ActivityCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityCreateForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ثبت گردید"


class ActivityUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityUpdateForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ویرایش شد"


class ActivityDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Activity
    template_name = 'government_accounts/confirm_delete.html'
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت حذف شد"


class ActivitySearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/activity_list.html'
    model = Activity
    context_object_name = "activities"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        if query is not None:
            search = Activity.objects.search(query)
            if search:
                return search
            else:
                not_found = True
        
        return Activity.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:activities_search'
        return context


