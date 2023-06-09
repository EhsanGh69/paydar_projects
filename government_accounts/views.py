from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
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

class ReceiveList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:receives_search'
        context['create_url'] = 'government_accounts:receive_create'
        context['persian_object_name'] = 'دریافت'
        return context


class ReceiveCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ثبت گردید"

    def get_form_kwargs(self):
        kwargs = super(ReceiveCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    

class ReceiveUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(ReceiveUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ReceiveDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        receive = get_object_or_404(Receive, pk=_id)
        return receive


class ReceiveSearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/receive_list.html'
    model = Receive
    context_object_name = "receives"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = Receive.objects.search(query).filter(receive_date__date__range=filter_date_values(date_filter)).all()
        else:
            search_result = Receive.objects.search(query).all()

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:receives_search'
        context['list_url'] = 'government_accounts:receives'
        return context


# Receive - End

# ---------------------------------------

# Organization - Start

class OrganizationList(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/organization_list.html'
    model = Organization
    context_object_name = "organizations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persian_object_name'] = 'ارگان'
        return context


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
    # model = Organization
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        organization = get_object_or_404(Organization, pk=_id)
        return organization


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
        context['create_url'] = 'government_accounts:payment_create'
        context['persian_object_name'] = 'پرداخت'
        return context


class PaymentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ثبت گردید"

    def get_form_kwargs(self):
        kwargs = super(PaymentCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class PaymentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(PaymentUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class PaymentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    # model = Payment
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        payment = get_object_or_404(Payment, pk=_id)
        return payment


class PaymentSearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = Payment.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter)).all()
        else:
            search_result = Payment.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:payments_search'
        context['list_url'] = 'government_accounts:payments'
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
        context['create_url'] = 'government_accounts:activity_create'
        context['persian_object_name'] = 'فعالیت'
        return context


class ActivityCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ثبت گردید"

    def get_form_kwargs(self):
        kwargs = super(ActivityCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ActivityUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(ActivityUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ActivityDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        activity = get_object_or_404(Activity, pk=_id)
        return activity


class ActivitySearch(LoginRequiredMixin, ListView):
    template_name = 'government_accounts/activity_list.html'
    model = Activity
    context_object_name = "activities"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        activity_filter = self.request.GET.get('activity_result')

        global search_result
        if activity_filter != "all" and date_filter == 'all':
            search_result = Activity.objects.search(query).filter(activity_result=activity_filter).all()
        elif activity_filter == "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__date__range=filter_date_values(date_filter)).all()
        elif activity_filter != "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__date__range=filter_date_values(date_filter), activity_result=activity_filter).all()
        else:
            search_result = Activity.objects.search(query)

        if not search_result:
            not_found = True
            
        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:activities_search'
        context['list_url'] = 'government_accounts:activities'
        return context
    
# Activity - End
