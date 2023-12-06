from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values
from account.models import UserActionsLog
from .models import ( Contracts,  Proceedings,  Agreements,  BankReceipts,  ConditionStatements, RegisteredDocs, OfficialDocs)
from .forms import (ContractsForm, ProceedingsForm, AgreementsForm, BankReceiptsForm, ConditionStatementsForm,RegisteredDocsForm,OfficialDocsForm)



# Contracts - Start

class ContractsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_contracts'
    template_name = 'projects_docs/contracts_list.html'
    model = Contracts
    context_object_name = "contracts"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Contracts.objects.order_by(order_by).all()
        else:
            queryset = Contracts.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Contracts.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:contracts_search'
        context['create_url'] = 'projects_docs:contract_create'
        context['list_url'] = 'projects_docs:contracts'
        context['persian_object_name'] = 'قرارداد'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'related_to_project__title', 'طرف قرارداد': 'contract_party',
        'تاریخ قرارداد': '-contract_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ContractsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_contracts'
    model = Contracts
    template_name = 'projects_docs/contract_create_update.html'
    form_class = ContractsForm
    success_url = reverse_lazy("projects_docs:contracts")
    success_message = "قرارداد با موفقیت ثبت شد"

    def form_valid(self, form):
        related_to_project = form.cleaned_data.get('related_to_project')
        unrelated_to_project = form.cleaned_data.get('unrelated_to_project')
        if related_to_project is None and unrelated_to_project == '':
            form.errors['__all__'] = form.error_class(["لطفاً پروژه‌ایی را انتخاب کنید یا توضیح قرارداد غیرمرتبط با پروژه را وارد نمایید"])
            return super().form_invalid(form) # type: ignore
        else:
            UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک قرارداد جدید")
            return super().form_valid(form)


class ContractsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_contracts'
    model = Contracts
    template_name = 'projects_docs/contract_create_update.html'
    form_class = ContractsForm
    success_url = reverse_lazy("projects_docs:contracts")
    success_message = "قرارداد با موفقیت ویرایش شد"

    def form_valid(self, form):
        related_to_project = form.cleaned_data.get('related_to_project')
        unrelated_to_project = form.cleaned_data.get('unrelated_to_project')
        if related_to_project is None and unrelated_to_project == '':
            form.errors['__all__'] = form.error_class(["لطفاً پروژه‌ایی را انتخاب کنید یا توضیح قرارداد غیرمرتبط با پروژه را وارد نمایید"])
            return super().form_invalid(form) # type: ignore
        else:
            UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک قرارداد")
            return super().form_valid(form)


class ContractsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_contracts'
    success_url = reverse_lazy("projects_docs:contracts")
    success_message = "قرارداد با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        contract = get_object_or_404(Contracts, pk=_id)
        return contract
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک قرارداد")
        return super().form_valid(form)


class ContractsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_contracts'
    template_name = 'projects_docs/contracts_list.html'
    model = Contracts
    context_object_name = "contracts"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global contract_type_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        contract_type_filter = self.request.GET.get('contract_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if contract_type_filter != "all" and date_filter == "all":
            search_result = Contracts.objects.search(query).filter(contract_type=contract_type_filter).all() # type: ignore

        elif contract_type_filter == "all" and date_filter != "all":
            search_result = Contracts.objects.search(query).filter(contract_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif contract_type_filter != "all" and date_filter != "all":
            search_result = Contracts.objects.search(query).filter(contract_date__range=filter_date_values(date_filter), # type: ignore
                                                                    contract_type=contract_type_filter).all()
        else:
            search_result = Contracts.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:contracts_search'
        context['list_url'] = 'projects_docs:contracts'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'contract_type': contract_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'related_to_project__title', 'طرف قرارداد': 'contract_party',
        'تاریخ قرارداد': '-contract_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Contracts - End

# -----------------------------------------------

# Proceedings - Start


class ProceedingsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_proceedings'
    template_name = 'projects_docs/proceedings_list.html'
    model = Proceedings
    context_object_name = "proceedings"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Proceedings.objects.order_by(order_by).all()
        else:
            queryset = Proceedings.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Proceedings.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:proceedings_search'
        context['create_url'] = 'projects_docs:proceeding_create'
        context['list_url'] = 'projects_docs:proceedings'
        context['persian_object_name'] = 'صورت جلسه'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'طرف حساب': 'account_party',
        'تاریخ صورت جلسه': '-proceeding_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ProceedingsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_proceedings'
    model = Proceedings
    template_name = 'projects_docs/proceeding_create_update.html'
    form_class = ProceedingsForm
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت ثبت شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک صورت جلسه جدید")
        return super().form_valid(form)


class ProceedingsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_proceedings'
    model = Proceedings
    template_name = 'projects_docs/proceeding_create_update.html'
    form_class = ProceedingsForm
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک صورت جلسه")
        return super().form_valid(form)


class ProceedingsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_proceedings'
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        proceeding = get_object_or_404(Proceedings, pk=_id)
        return proceeding
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک صورت جلسه")
        return super().form_valid(form)


class ProceedingsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_proceedings'
    template_name = 'projects_docs/proceedings_list.html'
    model = Proceedings
    context_object_name = "proceedings"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global proceeding_type_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        proceeding_type_filter = self.request.GET.get('proceeding_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if proceeding_type_filter != "all" and date_filter == "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_type=proceeding_type_filter).all() # type: ignore

        elif proceeding_type_filter == "all" and date_filter != "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif proceeding_type_filter != "all" and date_filter != "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_date__range=filter_date_values(date_filter), # type: ignore
                                                                    proceeding_type=proceeding_type_filter).all()
        else:
            search_result = Proceedings.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:proceedings_search'
        context['list_url'] = 'projects_docs:proceedings'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'proceeding_type': proceeding_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'طرف حساب': 'account_party',
        'تاریخ صورت جلسه': '-proceeding_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Proceedings - End

# --------------------------------------------------

# Agreements - Start

class AgreementsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_agreements'
    template_name = 'projects_docs/agreements_list.html'
    model = Agreements
    context_object_name = "agreements"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Agreements.objects.order_by(order_by).all()
        else:
            queryset = Agreements.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Agreements.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:agreements_search'
        context['create_url'] = 'projects_docs:agreement_create'
        context['list_url'] = 'projects_docs:agreements'
        context['persian_object_name'] = 'توافق‌نامه'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'طرف حساب': 'account_party',
        'تاریخ توافق‌نامه': '-agreement_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class AgreementsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_agreements'
    model = Agreements
    template_name = 'projects_docs/agreement_create_update.html'
    form_class = AgreementsForm
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت ثبت شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک توافق‌نامه جدید")
        return super().form_valid(form)


class AgreementsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_agreements'
    model = Agreements
    template_name = 'projects_docs/agreement_create_update.html'
    form_class = AgreementsForm
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک توافق‌نامه")
        return super().form_valid(form)


class AgreementsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_agreements'
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        agreement = get_object_or_404(Agreements, pk=_id)
        return agreement
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک توافق‌نامه")
        return super().form_valid(form)


class AgreementsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_agreements'
    template_name = 'projects_docs/agreements_list.html'
    model = Agreements
    context_object_name = "agreements"
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
            search_result = Agreements.objects.search(query).filter(agreement_date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Agreements.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:agreements_search'
        context['list_url'] = 'projects_docs:agreements'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'طرف حساب': 'account_party',
        'تاریخ توافق‌نامه': '-agreement_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Agreements - End

# -----------------------------------------------------

# BankReceipts - Start

class BankReceiptsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_bankreceipts'
    template_name = 'projects_docs/bank_receipts_list.html'
    model = BankReceipts
    context_object_name = "bank_receipts"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = BankReceipts.objects.order_by(order_by).all()
        else:
            queryset = BankReceipts.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = BankReceipts.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:bank_receipts_search'
        context['create_url'] = 'projects_docs:bank_receipt_create'
        context['list_url'] = 'projects_docs:bank_receipts'
        context['persian_object_name'] = 'رسید بانکی'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'تاریخ': '-receipt_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class BankReceiptsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_bankreceipts'
    model = BankReceipts
    template_name = 'projects_docs/bank_receipt_create_update.html'
    form_class = BankReceiptsForm
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت ثبت شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک رسید بانکی جدید")
        return super().form_valid(form)


class BankReceiptsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_bankreceipts'
    model = BankReceipts
    template_name = 'projects_docs/bank_receipt_create_update.html'
    form_class = BankReceiptsForm
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک رسید بانکی")
        return super().form_valid(form)


class BankReceiptsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_bankreceipts'
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        bank_receipt = get_object_or_404(BankReceipts, pk=_id)
        return bank_receipt
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک رسید بانکی")
        return super().form_valid(form)


class BankReceiptsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_bankreceipts'
    template_name = 'projects_docs/bank_receipts_list.html'
    model = BankReceipts
    context_object_name = "bank_receipts"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global receipt_type_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        receipt_type_filter = self.request.GET.get('receipt_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if receipt_type_filter != "all" and date_filter == "all":
            search_result = BankReceipts.objects.search(query).filter(receive_or_pay=receipt_type_filter).all() # type: ignore

        elif receipt_type_filter == "all" and date_filter != "all":
            search_result = BankReceipts.objects.search(query).filter(receipt_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif receipt_type_filter != "all" and date_filter != "all":
            search_result = BankReceipts.objects.search(query).filter(receipt_date__range=filter_date_values(date_filter), # type: ignore
                                                                    receive_or_pay=receipt_type_filter).all()
        else:
            search_result = BankReceipts.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:bank_receipts_search'
        context['list_url'] = 'projects_docs:bank_receipts'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'receipt_type': receipt_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'تاریخ': '-receipt_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# BankReceipts - End

# --------------------------------------------------------

# ConditionStatements - Start

class ConditionStatementsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_conditionstatements'
    template_name = 'projects_docs/condition_statements_list.html'
    model = ConditionStatements
    context_object_name = "condition_statements"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = ConditionStatements.objects.order_by(order_by).all()
        else:
            queryset = ConditionStatements.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = ConditionStatements.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:condition_statements_search'
        context['create_url'] = 'projects_docs:condition_statement_create'
        context['list_url'] = 'projects_docs:condition_statements'
        context['persian_object_name'] = 'صورت وضعیت'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'پیمانکار': 'contractor__full_name' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ConditionStatementsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_conditionstatements'
    model = ConditionStatements
    template_name = 'projects_docs/condition_statement_create_update.html'
    form_class = ConditionStatementsForm
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت ثبت شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک صورت وضعیت جدید")
        return super().form_valid(form)


class ConditionStatementsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_conditionstatements'
    model = ConditionStatements
    template_name = 'projects_docs/condition_statement_create_update.html'
    form_class = ConditionStatementsForm
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک صورت وضعیت")
        return super().form_valid(form)


class ConditionStatementsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_conditionstatements'
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        condition_statement = get_object_or_404(ConditionStatements, pk=_id)
        return condition_statement
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک صورت وضعیت")
        return super().form_valid(form)


class ConditionStatementsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_conditionstatements'
    template_name = 'projects_docs/condition_statements_list.html'
    model = ConditionStatements
    context_object_name = "condition_statements"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global accounting_confirm_filter
        global management_confirm_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        accounting_confirm_filter = self.request.GET.get('accounting_confirm')
        management_confirm_filter = self.request.GET.get('management_confirm')
        order_by = self.request.GET.get('order_by')

        global search_result

        if accounting_confirm_filter != "all" and management_confirm_filter == "all":
            search_result = ConditionStatements.objects.search(query).filter(accounting_confirm=accounting_confirm_filter).all() # type: ignore

        elif accounting_confirm_filter == "all" and management_confirm_filter != "all":
            search_result = ConditionStatements.objects.search(query).filter(management_confirm=management_confirm_filter).all() # type: ignore

        elif accounting_confirm_filter != "all" and management_confirm_filter != "all":
            search_result = ConditionStatements.objects.search(query).filter(accounting_confirm=accounting_confirm_filter, # type: ignore
                                                                    management_confirm=management_confirm_filter).all()
        else:
            search_result = ConditionStatements.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:condition_statements_search'
        context['list_url'] = 'projects_docs:condition_statements'
        context['list_filters'] = { 'data_search': query, 'accounting_confirm': accounting_confirm_filter, 
        'management_confirm': management_confirm_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'پیمانکار': 'contractor__full_name' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# ConditionStatements - End

# -----------------------------------------------------


# RegisteredDocs - Start

class RegisteredDocsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_registereddocs'
    template_name = 'projects_docs/registered_docs_list.html'
    model = RegisteredDocs
    context_object_name = "registered_docs"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = RegisteredDocs.objects.order_by(order_by).all()
        else:
            queryset = RegisteredDocs.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = RegisteredDocs.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:registered_docs_search'
        context['create_url'] = 'projects_docs:registered_doc_create'
        context['list_url'] = 'projects_docs:registered_docs'
        context['persian_object_name'] = 'سند ثبتی'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class RegisteredDocsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_registereddocs'
    model = RegisteredDocs
    template_name = 'projects_docs/registered_doc_create_update.html'
    form_class = RegisteredDocsForm
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت ثبت شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک سند ثبتی جدید")
        return super().form_valid(form)


class RegisteredDocsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_registereddocs'
    model = RegisteredDocs
    template_name = 'projects_docs/registered_doc_create_update.html'
    form_class = RegisteredDocsForm
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک سند ثبتی")
        return super().form_valid(form)


class RegisteredDocsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_registereddocs'
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        registered_doc = get_object_or_404(RegisteredDocs, pk=_id)
        return registered_doc
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک سند ثبتی")
        return super().form_valid(form)


class RegisteredDocsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_registereddocs'
    template_name = 'projects_docs/registered_docs_list.html'
    model = RegisteredDocs
    context_object_name = "registered_docs"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global doc_type_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        doc_type_filter = self.request.GET.get('doc_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if doc_type_filter != "all":
            search_result = RegisteredDocs.objects.search(query).filter(doc_type=doc_type_filter).all() # type: ignore
        else:
            search_result = RegisteredDocs.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:registered_docs_search'
        context['list_url'] = 'projects_docs:registered_docs'
        context['list_filters'] = { 'data_search': query, 'doc_type': doc_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# RegisteredDocs - End

# -----------------------------------------------------


# OfficialDocs - Start

class OfficialDocsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_officialdocs'
    template_name = 'projects_docs/official_docs_list.html'
    model = OfficialDocs
    context_object_name = "official_docs"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = OfficialDocs.objects.order_by(order_by).all()
        else:
            queryset = OfficialDocs.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = OfficialDocs.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:official_docs_search'
        context['create_url'] = 'projects_docs:official_doc_create'
        context['list_url'] = 'projects_docs:official_docs'
        context['persian_object_name'] = 'سند اداری'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'عنوان سند': 'doc_title',
        'تاریخ ارسال / دریافت': '-send_receive_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class OfficialDocsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects_docs.add_officialdocs'
    model = OfficialDocs
    template_name = 'projects_docs/official_doc_create_update.html'
    form_class = OfficialDocsForm
    success_url = reverse_lazy("projects_docs:official_docs")
    success_message = "سند اداری با موفقیت ثبت شد"

    def form_valid(self, form):
        doc_type = form.cleaned_data.get('doc_type')
        letter_type = form.cleaned_data.get('letter_type')
        license_type = form.cleaned_data.get('license_type')
        if doc_type == "let" and letter_type is None:
            form.add_error('letter_type', 'لطفا نوع نامه را انتخاب کنید')
            return super().form_invalid(form) # type: ignore
        elif doc_type == "lic" and license_type is None:
            form.add_error('license_type', 'لطفا نوع پروانه را انتخاب کنید')
            return super().form_invalid(form) # type: ignore
        else:
            UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک سند اداری جدید")
            return super().form_valid(form)


class OfficialDocsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects_docs.change_officialdocs'
    model = OfficialDocs
    template_name = 'projects_docs/official_doc_create_update.html'
    form_class = OfficialDocsForm
    success_url = reverse_lazy("projects_docs:official_docs")
    success_message = "سند اداری با موفقیت ویرایش شد"

    def form_valid(self, form):
        doc_type = form.cleaned_data.get('doc_type')
        letter_type = form.cleaned_data.get('letter_type')
        license_type = form.cleaned_data.get('license_type')
        if doc_type == "let" and letter_type is None:
            form.add_error('letter_type', 'لطفا نوع نامه را انتخاب کنید')
            return super().form_invalid(form) # type: ignore
        elif doc_type == "lic" and license_type is None:
            form.add_error('license_type', 'لطفا نوع پروانه را انتخاب کنید')
            return super().form_invalid(form) # type: ignore
        else:
            UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک سند اداری")
            return super().form_valid(form)


class OfficialDocsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects_docs.delete_officialdocs'
    success_url = reverse_lazy("projects_docs:official_docs")
    success_message = "سند اداری با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        official_doc = get_object_or_404(OfficialDocs, pk=_id)
        return official_doc
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک سند اداری")
        return super().form_valid(form)


class OfficialDocsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects_docs.view_officialdocs'
    template_name = 'projects_docs/official_docs_list.html'
    model = OfficialDocs
    context_object_name = "official_docs"
    paginate_by = 1

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global doc_type_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        doc_type_filter = self.request.GET.get('doc_type')
        order_by = self.request.GET.get('order_by')

        global search_result

        if doc_type_filter != "all" and doc_type_filter in ['let', 'lic', 'crt'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(doc_type=doc_type_filter).all() # type: ignore

        elif doc_type_filter != "all" and doc_type_filter in ['snd', 'rec'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(letter_type=doc_type_filter).all() # type: ignore

        elif doc_type_filter != "all" and doc_type_filter in ['des', 'con', 'dac', 'tci'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(license_type=doc_type_filter).all() # type: ignore

        elif doc_type_filter == "all" and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif doc_type_filter != "all" and doc_type_filter in ['let', 'lic', 'crt'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter), # type: ignore
                                                                    doc_type=doc_type_filter).all()
            
        elif doc_type_filter != "all" and doc_type_filter in ['snd', 'rec'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter), # type: ignore
                                                                    letter_type=doc_type_filter).all()
            
        elif doc_type_filter != "all" and doc_type_filter in ['des', 'con', 'dac', 'tci'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter), # type: ignore
                                                                    license_type=doc_type_filter).all()
        else:
            search_result = OfficialDocs.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects_docs:official_docs_search'
        context['list_url'] = 'projects_docs:official_docs'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'doc_type': doc_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'عنوان سند': 'doc_title',
        'تاریخ ارسال/دریافت': '-send_receive_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# OfficialDocs - End

# -----------------------------------------------------