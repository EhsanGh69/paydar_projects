from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from utils.tools import filter_date_values
from account.models import UserActionsLog
from .models import Receive, Organization, Payment, Activity
from .forms import ReceiveForm, OrganizationForm, PaymentForm, ActivityForm


# Organization - Start

class OrganizationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_organization'
    template_name = 'government_accounts/organization_list.html'
    model = Organization
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.order_by('organization_name').all()

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

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="افزودن یک ارگان جدید")
        return super().form_valid(form)
    

class OrganizationUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_organization'
    model = Organization
    template_name = 'government_accounts/organization_create_update.html'
    form_class = OrganizationForm
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک ارگان")
        return super().form_valid(form)


class OrganizationDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_organization'
    success_url = reverse_lazy("government_accounts:organizations")
    success_message = "ارگان با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        organization = get_object_or_404(Organization, pk=_id)
        return organization
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک ارگان")
        return super().form_valid(form)


# Organization - End

# ---------------------------------------------

# Receive - Start

class ReceiveList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_receive'
    model = Receive
    context_object_name = "receives"
    paginate_by = 9
    
    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Receive.objects.order_by(order_by).all()
        else:
            queryset = Receive.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Receive.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:receives_search'
        context['create_url'] = 'government_accounts:receive_create'
        context['list_url'] = 'government_accounts:receives'
        context['persian_object_name'] = 'دریافت'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'دریافت بابت': 'receive_for', 'تاریخ دریافت': '-receive_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class ReceiveCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_receive'
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک دریافت دولتی جدید")
        return super().form_valid(form)
    

class ReceiveUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_receive'
    model = Receive
    template_name = 'government_accounts/receive_create_update.html'
    form_class = ReceiveForm
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک دریافت دولتی")
        return super().form_valid(form)


class ReceiveDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_receive'
    success_url = reverse_lazy("government_accounts:receives")
    success_message = "دریافت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        receive = get_object_or_404(Receive, pk=_id)
        return receive
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک دریافت دولتی")
        return super().form_valid(form)


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
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        order_by = self.request.GET.get('order_by')

        global search_result
        if date_filter != "all":
            search_result = Receive.objects.search(query).filter(receive_date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Receive.objects.search(query).all() # type: ignore

        if not search_result:
            not_found = True
        elif order_by is not None and order_by != "none":
            search_result = search_result.order_by(order_by).all()
        else:
            search_result = search_result.order_by('-id').all()

        return search_result
        
    def get_context_data(self, **kwargs):
        records_count = search_result.count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:receives_search'
        context['list_url'] = 'government_accounts:receives'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'دریافت بابت': 'receive_for', 'تاریخ دریافت': '-receive_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Receive - End

# ---------------------------------------

# Payment - Start

class PaymentList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'government_accounts.view_payment'
    template_name = 'government_accounts/payment_list.html'
    model = Payment
    context_object_name = "payments"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Payment.objects.order_by(order_by).all()
        else:
            queryset = Payment.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Payment.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:payments_search'
        context['create_url'] = 'government_accounts:payment_create'
        context['list_url'] = 'government_accounts:payments'
        context['persian_object_name'] = 'پرداخت'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'پرداخت بابت': 'payment_for', 'تاریخ پرداخت': '-payment_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class PaymentCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_payment'
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک پرداخت دولتی جدید")
        return super().form_valid(form)


class PaymentUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_payment'
    model = Payment
    template_name = 'government_accounts/payment_create_update.html'
    form_class = PaymentForm
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک پرداخت دولتی")
        return super().form_valid(form)


class PaymentDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_payment'
    success_url = reverse_lazy("government_accounts:payments")
    success_message = "پرداخت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        payment = get_object_or_404(Payment, pk=_id)
        return payment
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک پرداخت دولتی")
        return super().form_valid(form)


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
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        order_by = self.request.GET.get('order_by')

        global search_result
        if date_filter != "all":
            search_result = Payment.objects.search(query).filter(payment_date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Payment.objects.search(query) # type: ignore

        if not search_result:
            not_found = True
        elif order_by is not None and order_by != "none":
            search_result = search_result.order_by(order_by).all()
        else:
            search_result = search_result.order_by('-id').all()

        return search_result
        
    def get_context_data(self, **kwargs):
        records_count = search_result.count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:payments_search'
        context['list_url'] = 'government_accounts:payments'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'پرداخت بابت': 'payment_for', 'تاریخ پرداخت': '-payment_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
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
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Activity.objects.order_by(order_by).all()
        else:
            queryset = Activity.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Activity.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'government_accounts:activities_search'
        context['create_url'] = 'government_accounts:activity_create'
        context['list_url'] = 'government_accounts:activities'
        context['persian_object_name'] = 'فعالیت'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'نوع فعالیت': 'activity_type', 'تاریخ فعالیت': '-activity_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ActivityCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'government_accounts.add_activity'
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک فعالیت جدید")
        return super().form_valid(form)


class ActivityUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'government_accounts.change_activity'
    model = Activity
    template_name = 'government_accounts/activity_create_update.html'
    form_class = ActivityForm
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک فعالیت")
        return super().form_valid(form)


class ActivityDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'government_accounts.delete_activity'
    success_url = reverse_lazy("government_accounts:activities")
    success_message = "فعالیت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        activity = get_object_or_404(Activity, pk=_id)
        return activity
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک فعالیت")
        return super().form_valid(form)


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
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        activity_filter = self.request.GET.get('activity_result')
        order_by = self.request.GET.get('order_by')

        global search_result
        if activity_filter != "all" and date_filter == 'all':
            search_result = Activity.objects.search(query).filter(activity_result=activity_filter).all() # type: ignore
        elif activity_filter == "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__range=filter_date_values(date_filter)).all() # type: ignore
        elif activity_filter != "all" and date_filter != 'all':
            search_result = Activity.objects.search(query).filter(activity_date__range=filter_date_values(date_filter), activity_result=activity_filter).all() # type: ignore
        else:
            search_result = Activity.objects.search(query) # type: ignore

        if not search_result:
            not_found = True
        elif order_by is not None and order_by != "none":
            search_result = search_result.order_by(order_by).all()
        else:
            search_result = search_result.order_by('-id').all()
            
        return search_result
        
    def get_context_data(self, **kwargs):
        records_count = search_result.count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'government_accounts:activities_search'
        context['list_url'] = 'government_accounts:activities'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter,
        'activity_result':activity_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'ارگان' :'organization__organization_name', 'پروژه': 'project__title',
        'نوع فعالیت': 'activity_type', 'تاریخ فعالیت': '-activity_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    
# Activity - End