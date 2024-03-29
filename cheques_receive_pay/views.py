from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values, fund_validation, cash_box_validation, image_size_validation
from account.models import UserActionsLog
from .models import Cheques, Fund, ReceivePay, CashBox
from .forms import ChequesForm, FundForm, ReceivePayForm, CashBoxForm




# Cheques - Start

class ChequesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cheques'
    template_name = 'cheques_receive_pay/cheques_list.html'
    model = Cheques
    context_object_name = "cheques"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Cheques.objects.order_by(order_by).all()
        else:
            queryset = Cheques.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Cheques.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:cheques_search'
        context['create_url'] = 'cheques_receive_pay:cheque_create'
        context['list_url'] = 'cheques_receive_pay:cheques'
        context['persian_object_name'] = 'چک'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'بابت': 'cheque_for', 'بانک و شعبه': 'bank_branch', 
        'تاریخ صدور / دریافت': '-export_receive_date', 'تاریخ سررسید': 'due_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ChequesCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_cheques'
    template_name = 'cheques_receive_pay/cheque_create_update.html'
    model = Cheques
    form_class = ChequesForm
    success_url = reverse_lazy("cheques_receive_pay:cheques")

    def form_valid(self, form):
        result_validation = image_size_validation(form, ['cheque_image'])
        if not result_validation:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('cheque_type'), ""
        if obj_type == "exp":
            self.success_message = "چک پرداختی با موفقیت ثبت شد"
            log_content="ثبت چک پرداختی جدید"
        else:
            self.success_message = "چک دریافتی با موفقیت ثبت شد"
            log_content="ثبت چک دریافتی جدید"
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content=log_content)
        return super().form_valid(form)

    def form_invalid(self, form):
        result_validation = image_size_validation(form, ['cheque_image'])
        return self.render_to_response(self.get_context_data(size_valid=result_validation, form_invalid=True))


class ChequesUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_cheques'
    template_name = 'cheques_receive_pay/cheque_create_update.html'
    model = Cheques
    form_class = ChequesForm
    success_url = reverse_lazy("cheques_receive_pay:cheques")

    def form_valid(self, form):
        result_validation = image_size_validation(form, ['cheque_image'])
        if not result_validation:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('cheque_type'), ""
        if obj_type == "exp":
            self.success_message = "چک پرداختی با موفقیت ویرایش شد"
            log_content="ویرایش چک پرداختی"
        else:
            self.success_message = "چک دریافتی با موفقیت ویرایش شد"
            log_content="ویرایش چک دریافتی"
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content=log_content)
        return super().form_valid(form)

    def form_invalid(self, form):
        result_validation = image_size_validation(form, ['cheque_image'])
        return self.render_to_response(self.get_context_data(size_valid=result_validation, form_invalid=True))


class ChequesDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_cheques'
    success_url = reverse_lazy("cheques_receive_pay:cheques")

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cheque = get_object_or_404(Cheques, pk=_id)
        return cheque
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        obj, log_content = get_object_or_404(Cheques, pk=id), ""
        if obj.cheque_type == "exp":
            self.success_message = "چک پرداختی با موفقیت حذف شد"
            log_content="حذف چک پرداختی"
        else:
            self.success_message = "چک دریافتی با موفقیت حذف شد"
            log_content="حذف چک دریافتی"
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content=log_content)
        return super().form_valid(form)
    

class ChequesSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cheques'
    template_name = 'cheques_receive_pay/cheques_list.html'
    model = Cheques
    context_object_name = "cheques"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global cheque_type_filter
        global order_by
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        cheque_type_filter = self.request.GET.get('cheque_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if cheque_type_filter != "all" and date_filter == "all":
            search_result = Cheques.objects.search(query).filter(cheque_type=cheque_type_filter).all() # type: ignore

        elif cheque_type_filter == "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif cheque_type_filter != "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__range=filter_date_values(date_filter), cheque_type=cheque_type_filter).all() # type: ignore
        else:
            search_result = Cheques.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

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
        context['search_url'] = 'cheques_receive_pay:cheques_search'
        context['list_url'] = 'cheques_receive_pay:cheques'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter,
        'cheque_type': cheque_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'بابت': 'cheque_for', 'بانک و شعبه': 'bank_branch', 
        'تاریخ صدور / دریافت': '-export_receive_date', 'تاریخ سررسید': 'due_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Cheques - End

# -----------------------------------------------

# Fund - Start


class FundList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_fund'
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Fund
    context_object_name = "funds"
    paginate_by = 4

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Fund.objects.order_by(order_by).all()
        else:
            queryset = Fund.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        fund_names = []
        if queryset:
            for obj in queryset:
                fund_names.append(obj.full_name) # type: ignore
        records_count = Fund.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 4:
            record_number = 4
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['create_url'] = 'cheques_receive_pay:fund_create'
        context['list_url'] = 'cheques_receive_pay:funds'
        context['persian_object_name'] = 'تنخواه'
        context['fund_names'] = sorted(list(set(fund_names)))
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'نام و نام خانوادگی' : 'full_name', 'نوع عملیات': '-operation_type',
        'تاریخ برداشت': '-removal_date', 'تاریخ واریز': '-charge_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class FundCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_fund'
    template_name = 'cheques_receive_pay/fund_create_update.html'
    model = Fund
    form_class = FundForm
    success_url = reverse_lazy("cheques_receive_pay:funds")

    def get_form_kwargs(self):
        kwargs = super(FundCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    
    def form_valid(self, form):
        validation_result = fund_validation(form=form, model=Fund, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('operation_type'), ""
        if obj_type == "rem":
            self.success_message = "برداشت از تنخواه با موفقیت ثبت شد"
            log_content="ثبت برداشت از تنخواه"
        else:
            self.success_message = "واریز به تنخواه با موفقیت ثبت شد"
            log_content="ثبت واریز به تنخواه"
        
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content=log_content)
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        queryset = Fund.objects.all()
        fund_names = []
        if queryset:
            for obj in queryset:
                fund_names.append(obj.full_name)
        context = super().get_context_data(**kwargs)
        context['fund_names'] = sorted(list(set(fund_names)))
        return context
        

class FundUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_fund'
    template_name = 'cheques_receive_pay/fund_create_update.html'
    model = Fund
    form_class = FundForm
    success_url = reverse_lazy("cheques_receive_pay:funds")

    def get_form_kwargs(self):
        kwargs = super(FundUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    
    def form_valid(self, form):
        validation_result = fund_validation(form=form, model=Fund, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('operation_type'), ""
        if obj_type == "rem":
            self.success_message = "برداشت از تنخواه با موفقیت ویرایش شد"
            log_content="ویرایش برداشت از تنخواه"
        else:
            self.success_message = "واریز به تنخواه با موفقیت ویرایش شد"
            log_content="ویرایش واریز به تنخواه"
        
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content=log_content)
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        queryset = Fund.objects.all()
        fund_names = []
        if queryset:
            for obj in queryset:
                fund_names.append(obj.full_name)
        context = super().get_context_data(**kwargs)
        context['fund_names'] = sorted(list(set(fund_names)))
        return context

    
class FundDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_fund'
    success_url = reverse_lazy("cheques_receive_pay:funds")

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        fund = get_object_or_404(Fund, pk=_id)
        return fund
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        obj, log_content = get_object_or_404(Fund, pk=id), ""
        if obj.operation_type == "rem":
            self.success_message = "برداشت از تنخواه با موفقیت حذف شد"
            log_content="حذف برداشت از تنخواه"
        else:
            self.success_message = "واریز به تنخواه با موفقیت حذف شد"
            log_content="حذف واریز به تنخواه"
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content=log_content)
        return super().form_valid(form)
    

class FundSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_fund'
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Fund
    context_object_name = "funds"
    paginate_by = 4

    def get_queryset(self):
        global not_found
        global query
        global operation_type_filter
        global order_by
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        operation_type_filter = self.request.GET.get('operation_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if operation_type_filter != "all":
            search_result = Fund.objects.search(query).filter(operation_type=operation_type_filter).all() # type: ignore
        else:
            search_result = Fund.objects.search(query) # type: ignore

        if not search_result:
            not_found = True
        elif order_by is not None and order_by != "none":
            search_result = search_result.order_by(order_by).all()
        else:
            search_result = search_result.order_by('-id').all()

        return search_result
        
    def get_context_data(self, **kwargs):
        fund_names = []
        if search_result:
            for obj in search_result:
                fund_names.append(obj.full_name) # type: ignore
        records_count = search_result.count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 4:
            record_number = 4
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['list_url'] = 'cheques_receive_pay:funds'
        context['fund_names'] = sorted(list(set(fund_names)))
        context['list_filters'] = { 'data_search': query, 'operation_type': operation_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'نام و نام خانوادگی' : 'full_name', 'نوع عملیات': '-operation_type',
        'تاریخ برداشت': '-removal_date', 'تاریخ واریز': '-charge_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Fund - End

# -------------------------------------------------


# ReceivePay - Start

class ReceivePayList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_receivepay'
    template_name = 'cheques_receive_pay/receive_pays_list.html'
    model = ReceivePay
    context_object_name = "receive_pays"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = ReceivePay.objects.order_by(order_by).all()
        else:
            queryset = ReceivePay.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = ReceivePay.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:receive_pays_search'
        context['create_url'] = 'cheques_receive_pay:receive_pay_create'
        context['list_url'] = 'cheques_receive_pay:receive_pays'
        context['persian_object_name'] = 'دریافت / پرداخت'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'بابت': 'regard_to', 'تاریخ': 'date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ReceivePayCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_receivepay'
    template_name = 'cheques_receive_pay/receive_pay_create_update.html'
    model = ReceivePay
    form_class = ReceivePayForm
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")

    def form_valid(self, form):
        organ = form.cleaned_data.get('organ')
        contractor = form.cleaned_data.get('contractor')
        supplier = form.cleaned_data.get('supplier')
        personnel = form.cleaned_data.get('personnel')
        result_validation = image_size_validation(form, ['receipt_image'])
        if not organ and (not contractor or not supplier or not personnel):
            form.errors['__all__'] = form.error_class(["لطفاً طرف حساب دولتی یا یکی از طرف حساب‌های غیردولتی را انتخاب کنید"])
            return super().form_invalid(form)
        if not result_validation:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('receive_pay'), ""
        if obj_type == "rec":
            self.success_message = "مبلغ پرداختی با موفقیت ثبت شد"
            log_content="ثبت مبلغ پرداختی جدید"
        else:
            self.success_message = "مبلغ دریافتی با موفقیت ثبت شد"
            log_content="ثبت مبلغ دریافتی جدید"
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content=log_content)
        return super().form_valid(form)

    def form_invalid(self, form):
        result_validation = image_size_validation(form, ['receipt_image'])
        return self.render_to_response(self.get_context_data(size_valid=result_validation, form_invalid=True))
    

class ReceivePayUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_receivepay'
    template_name = 'cheques_receive_pay/receive_pay_create_update.html'
    model = ReceivePay
    form_class = ReceivePayForm
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")

    def form_valid(self, form):
        organ = form.cleaned_data.get('organ')
        contractor = form.cleaned_data.get('contractor')
        supplier = form.cleaned_data.get('supplier')
        personnel = form.cleaned_data.get('personnel')
        result_validation = image_size_validation(form, ['receipt_image'])
        if not organ and (not contractor or not supplier or not personnel):
            form.errors['__all__'] = form.error_class(["لطفاً طرف حساب دولتی یا یکی از طرف حساب‌های غیردولتی را انتخاب کنید"])
            return super().form_invalid(form)
        if not result_validation:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('receive_pay'), ""
        if obj_type == "rec":
            self.success_message = "مبلغ پرداختی با موفقیت ویرایش شد"
            log_content="ویرایش مبلغ پرداختی"
        else:
            self.success_message = "مبلغ دریافتی با موفقیت ویرایش شد"
            log_content="ویرایش مبلغ دریافتی"
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content=log_content)
        return super().form_valid(form)

    def form_invalid(self, form):
        result_validation = image_size_validation(form, ['receipt_image'])
        return self.render_to_response(self.get_context_data(size_valid=result_validation, form_invalid=True))


class ReceivePayDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_receivepay'
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")
    success_message = "دریافت / پرداخت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        receive_pay = get_object_or_404(ReceivePay, pk=_id)
        return receive_pay
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        obj, log_content = get_object_or_404(ReceivePay, pk=id), ""
        if obj.receive_pay == "rec":
            self.success_message = "مبلغ پرداختی با موفقیت حذف شد"
            log_content="حذف مبلغ پرداختی"
        else:
            self.success_message = "مبلغ دریافتی با موفقیت حذف شد"
            log_content="حذف مبلغ دریافتی"
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content=log_content)
        return super().form_valid(form)
    

class ReceivePaySearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_receivepay'
    template_name = 'cheques_receive_pay/receive_pays_list.html'
    model = ReceivePay
    context_object_name = "receive_pays"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global order_by
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        order_by = self.request.GET.get('order_by')

        global search_result

        if date_filter != "all":
            search_result = ReceivePay.objects.search(query).filter(date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = ReceivePay.objects.search(query) # type: ignore

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
        context['search_url'] = 'cheques_receive_pay:receive_pays_search'
        context['list_url'] = 'cheques_receive_pay:receive_pays'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'بابت': 'regard_to', 'تاریخ': 'date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# ReceivePay - End

# ------------------------------------------------


# CashBox - Start


class CashBoxList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cashbox'
    template_name = 'cheques_receive_pay/cash_boxes_list.html'
    model = CashBox
    context_object_name = "cash_boxes"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = CashBox.objects.order_by(order_by).all()
        else:
            queryset = CashBox.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = CashBox.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:cash_boxes_search'
        context['create_url'] = 'cheques_receive_pay:cash_box_create'
        context['list_url'] = 'cheques_receive_pay:cash_boxes'
        context['persian_object_name'] = 'صندوق'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'تاریخ واریز': '-settle_date', 'تاریخ برداشت': '-removal_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class CashBoxCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_cashbox'
    template_name = 'cheques_receive_pay/cash_box_create_update.html'
    model = CashBox
    form_class = CashBoxForm
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")

    def form_valid(self, form):
        validation_result = cash_box_validation(form=form, model=CashBox, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form)
        obj_type, log_content = form.cleaned_data.get('operation_type'), ""
        if obj_type == "rem":
            self.success_message = "برداشت از صندوق با موفقیت ثبت شد"
            log_content="ثبت برداشت از صندوق"
        else:
            self.success_message = "واریز به صندوق با موفقیت ثبت شد"
            log_content="ثبت واریز به صندوق"
        
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content=log_content)
        return super().form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super(CashBoxCreate, self).get_form_kwargs() # type: ignore
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
        

class CashBoxUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_cashbox'
    template_name = 'cheques_receive_pay/cash_box_create_update.html'
    model = CashBox
    form_class = CashBoxForm
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")

    def form_valid(self, form):
        validation_result = cash_box_validation(form=form, model=CashBox, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form)  
        obj_type, log_content = form.cleaned_data.get('operation_type'), ""
        if obj_type == "rem":
            self.success_message = "برداشت از صندوق با موفقیت ویرایش شد"
            log_content="ویرایش برداشت از صندوق"
        else:
            self.success_message = "واریز به صندوق با موفقیت ویرایش شد"
            log_content="ویرایش واریز به صندوق"
        
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content=log_content)
        return super().form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super(CashBoxUpdate, self).get_form_kwargs() # type: ignore
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class CashBoxDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_cashbox'
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cash_box = get_object_or_404(CashBox, pk=_id)
        return cash_box
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        obj, log_content = get_object_or_404(CashBox, pk=id), ""
        if obj.operation_type == "rem":
            self.success_message = "برداشت از صندوق با موفقیت حذف شد"
            log_content="حذف برداشت از صندوق"
        else:
            self.success_message = "واریز به صندوق با موفقیت حذف شد"
            log_content="حذف واریز به صندوق"
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content=log_content)
        return super().form_valid(form)


class CashBoxSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cashbox'
    template_name = 'cheques_receive_pay/cash_boxes_list.html'
    model = CashBox
    context_object_name = "cash_boxes"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global operation_type_filter
        global order_by
        not_found = False
        operation_type_filter = self.request.GET.get('operation_type')
        order_by = self.request.GET.get('order_by')

        global search_result
        if operation_type_filter != "all":
            search_result = CashBox.objects.filter(operation_type=operation_type_filter).all() # type: ignore

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
        context['search_url'] = 'cheques_receive_pay:cash_boxes_search'
        context['list_url'] = 'cheques_receive_pay:cash_boxes'
        context['list_filters'] = { 'operation_type': operation_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'تاریخ واریز': '-settle_date', 'تاریخ برداشت': '-removal_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# CashBox - End