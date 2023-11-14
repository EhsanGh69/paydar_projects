from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from utils.tools import filter_date_values
from .models import Receive, Organization, Payment, Activity
from .forms import (
    ReceiveForm, 
    OrganizationForm,
    PaymentForm,
    ActivityForm
)

# Receive - Start

class ReceiveList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_receive'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9

    def get_queryset(self):
        return Receive.objects.order_by('-receive_date', '-create_record').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:receives_search'
        context['create_url'] = 'government_accounts:receive_create'
        context['persian_object_name'] = 'دریافت'
        return context


class ReceiveCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_receive'
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ثبت گردید"
    

class ReceiveUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_receive'
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ویرایش شد"


class ReceiveDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_receive'
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        receive = get_object_or_404(Receive, pk=_id)
        return receive


class ReceiveSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_receive'
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = Receive.objects.search(query).filter(receive_date__date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Receive.objects.search(query).all() # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:receives_search'
        context['list_url'] = 'government_accounts:receives'
        context['query'] = query
        context['date_filter'] = date_filter
        return context


# Receive - End

# ---------------------------------------

# Organization - Start

class OrganizationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_organization'
    template_name = 'government_accounts/organization_list.html'
    model = Organization
    context_object_name = "organizations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persian_object_name'] = 'ارگان'
        return context


class OrganizationCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_organization'
    model = Organization
    template_name = 'government_accounts/organization_create_update.html'
    form_class = OrganizationForm
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت افزوده شد"
    

class OrganizationUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_organization'
    model = Organization
    template_name = 'government_accounts/organization_create_update.html'
    form_class = OrganizationForm
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت ویرایش شد"


class OrganizationDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_organization'
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        organization = get_object_or_404(Organization, pk=_id)
        return organization


# Organization - End


# ---------------------------------------------

# Payment - Start


class PaymentList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_payment'
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"
    paginate_by = 9

    def get_queryset(self):
        return Payment.objects.order_by('-payment_date', '-create_record').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:payments_search'
        context['create_url'] = 'government_accounts:payment_create'
        context['persian_object_name'] = 'پرداخت'
        return context


class PaymentCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_payment'
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ثبت گردید"


class PaymentUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_payment'
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ویرایش شد"


class PaymentDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_payment'
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        payment = get_object_or_404(Payment, pk=_id)
        return payment


class PaymentSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_payment'
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = Payment.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Payment.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:payments_search'
        context['list_url'] = 'government_accounts:payments'
        context['query'] = query
        context['date_filter'] = date_filter
        return context

# Payment - End

# ---------------------------------------------

# Activity - Start

class ActivityList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_activity'
    template_name = 'government_accounts/activity_list.html'
    model = Activity
    context_object_name = "activities"
    paginate_by = 9

    def get_queryset(self):
        return Activity.objects.order_by('-activity_date', '-create_record').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:activities_search'
        context['create_url'] = 'government_accounts:activity_create'
        context['persian_object_name'] = 'فعالیت'
        return context


class ActivityCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_activity'
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ثبت گردید"


class ActivityUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_activity'
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ویرایش شد"


class ActivityDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_activity'
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        activity = get_object_or_404(Activity, pk=_id)
        return activity


class ActivitySearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_activity'
    template_name = 'government_accounts/activity_list.html'
    model = Activity
    context_object_name = "activities"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global activity_filter
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        activity_filter = self.request.GET.get('activity_result')

        global search_result
        if activity_filter != "all" and date_filter == 'all':
            search_result = Activity.objects.search(query).filter(activity_result=activity_filter).all() # type: ignore
        elif activity_filter == "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__date__range=filter_date_values(date_filter)).all() # type: ignore
        elif activity_filter != "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__date__range=filter_date_values(date_filter), activity_result=activity_filter).all() # type: ignore
        else:
            search_result = Activity.objects.search(query) # type: ignore

        if not search_result:
            not_found = True
            
        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:activities_search'
        context['list_url'] = 'government_accounts:activities'
        context['query'] = query
        context['date_filter'] = date_filter
        context['activity_filter'] = activity_filter
        return context
    
# Activity - End
