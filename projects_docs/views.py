from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values
from .models import (
    Contracts, 
    Proceedings, 
    Agreements, 
    BankReceipts, 
    ConditionStatements,
    RegisteredDocs,
    OfficialDocs
)
from .forms import (
    ContractsForm, 
    ProceedingsForm, 
    AgreementsForm, 
    BankReceiptsForm, 
    ConditionStatementsForm,
    RegisteredDocsForm,
    OfficialDocsForm
)




# Contracts - Start

class ContractsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/contracts_list.html'
    model = Contracts
    context_object_name = "contracts"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:contracts_search'
        context['create_url'] = 'projects_docs:contract_create'
        context['persian_object_name'] = 'قرارداد'
        return context


class ContractsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class ContractsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class ContractsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:contracts")
    success_message = "قرارداد با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        contract = get_object_or_404(Contracts, pk=_id)
        return contract


class ContractsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/contracts_list.html'
    model = Contracts
    context_object_name = "contracts"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        contract_type_filter = self.request.GET.get('contract_type')

        global search_result

        if contract_type_filter != "all" and date_filter == "all":
            search_result = Contracts.objects.search(query).filter(contract_type=contract_type_filter).all()

        elif contract_type_filter == "all" and date_filter != "all":
            search_result = Contracts.objects.search(query).filter(contract_date__range=filter_date_values(date_filter)).all()

        elif contract_type_filter != "all" and date_filter != "all":
            search_result = Contracts.objects.search(query).filter(contract_date__range=filter_date_values(date_filter),
                                                                    contract_type=contract_type_filter).all()
        else:
            search_result = Contracts.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:contracts_search'
        context['list_url'] = 'projects_docs:contracts'
        return context


# Contracts - End

# -----------------------------------------------

# Proceedings - Start


class ProceedingsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/proceedings_list.html'
    model = Proceedings
    context_object_name = "proceedings"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:proceedings_search'
        context['create_url'] = 'projects_docs:proceeding_create'
        context['persian_object_name'] = 'صورت جلسه'
        return context


class ProceedingsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proceedings
    template_name = 'projects_docs/proceeding_create_update.html'
    form_class = ProceedingsForm
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت ثبت شد"


class ProceedingsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proceedings
    template_name = 'projects_docs/proceeding_create_update.html'
    form_class = ProceedingsForm
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت ویرایش شد"


class ProceedingsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:proceedings")
    success_message = "صورت جلسه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        proceeding = get_object_or_404(Proceedings, pk=_id)
        return proceeding


class ProceedingsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/proceedings_list.html'
    model = Proceedings
    context_object_name = "proceedings"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        proceeding_type_filter = self.request.GET.get('proceeding_type')

        global search_result

        if proceeding_type_filter != "all" and date_filter == "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_type=proceeding_type_filter).all()

        elif proceeding_type_filter == "all" and date_filter != "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_date__range=filter_date_values(date_filter)).all()

        elif proceeding_type_filter != "all" and date_filter != "all":
            search_result = Proceedings.objects.search(query).filter(proceeding_date__range=filter_date_values(date_filter),
                                                                    proceeding_type=proceeding_type_filter).all()
        else:
            search_result = Proceedings.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:proceedings_search'
        context['list_url'] = 'projects_docs:proceedings'
        return context


# Proceedings - End

# --------------------------------------------------

# Agreements - Start

class AgreementsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/agreements_list.html'
    model = Agreements
    context_object_name = "agreements"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:agreements_search'
        context['create_url'] = 'projects_docs:agreement_create'
        context['persian_object_name'] = 'توافق‌نامه'
        return context


class AgreementsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Agreements
    template_name = 'projects_docs/agreement_create_update.html'
    form_class = AgreementsForm
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت ثبت شد"


class AgreementsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Agreements
    template_name = 'projects_docs/agreement_create_update.html'
    form_class = AgreementsForm
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت ویرایش شد"


class AgreementsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:agreements")
    success_message = "توافق‌نامه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        agreement = get_object_or_404(Agreements, pk=_id)
        return agreement


class AgreementsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/agreements_list.html'
    model = Agreements
    context_object_name = "agreements"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result

        if date_filter != "all":
            search_result = Agreements.objects.search(query).filter(agreement_date__range=filter_date_values(date_filter)).all()
        else:
            search_result = Agreements.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:agreements_search'
        context['list_url'] = 'projects_docs:agreements'
        return context


# Agreements - End

# -----------------------------------------------------

# BankReceipts - Start

class BankReceiptsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/bank_receipts_list.html'
    model = BankReceipts
    context_object_name = "bank_receipts"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:bank_receipts_search'
        context['create_url'] = 'projects_docs:bank_receipt_create'
        context['persian_object_name'] = 'رسید بانکی'
        return context


class BankReceiptsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BankReceipts
    template_name = 'projects_docs/bank_receipt_create_update.html'
    form_class = BankReceiptsForm
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت ثبت شد"


class BankReceiptsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BankReceipts
    template_name = 'projects_docs/bank_receipt_create_update.html'
    form_class = BankReceiptsForm
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت ویرایش شد"


class BankReceiptsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:bank_receipts")
    success_message = "رسید بانکی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        bank_receipt = get_object_or_404(BankReceipts, pk=_id)
        return bank_receipt


class BankReceiptsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/bank_receipts_list.html'
    model = BankReceipts
    context_object_name = "bank_receipts"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        receipt_type_filter = self.request.GET.get('receipt_type')

        global search_result

        if receipt_type_filter != "all" and date_filter == "all":
            search_result = BankReceipts.objects.search(query).filter(receive_or_pay=receipt_type_filter).all()

        elif receipt_type_filter == "all" and date_filter != "all":
            search_result = BankReceipts.objects.search(query).filter(receipt_date__range=filter_date_values(date_filter)).all()

        elif receipt_type_filter != "all" and date_filter != "all":
            search_result = BankReceipts.objects.search(query).filter(receipt_date__range=filter_date_values(date_filter),
                                                                    receive_or_pay=receipt_type_filter).all()
        else:
            search_result = BankReceipts.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:bank_receipts_search'
        context['list_url'] = 'projects_docs:bank_receipts'
        return context


# BankReceipts - End

# --------------------------------------------------------

# ConditionStatements - Start

class ConditionStatementsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/condition_statements_list.html'
    model = ConditionStatements
    context_object_name = "condition_statements"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:condition_statements_search'
        context['create_url'] = 'projects_docs:condition_statement_create'
        context['persian_object_name'] = 'صورت وضعیت'
        return context


class ConditionStatementsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ConditionStatements
    template_name = 'projects_docs/condition_statement_create_update.html'
    form_class = ConditionStatementsForm
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت ثبت شد"


class ConditionStatementsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ConditionStatements
    template_name = 'projects_docs/condition_statement_create_update.html'
    form_class = ConditionStatementsForm
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت ویرایش شد"


class ConditionStatementsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:condition_statements")
    success_message = "صورت وضعیت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        condition_statement = get_object_or_404(ConditionStatements, pk=_id)
        return condition_statement


class ConditionStatementsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/condition_statements_list.html'
    model = ConditionStatements
    context_object_name = "condition_statements"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        accounting_confirm_filter = self.request.GET.get('accounting_confirm')
        management_confirm_filter = self.request.GET.get('management_confirm')

        global search_result

        if accounting_confirm_filter != "all" and management_confirm_filter == "all":
            search_result = ConditionStatements.objects.search(query).filter(accounting_confirm=accounting_confirm_filter).all()

        elif accounting_confirm_filter == "all" and management_confirm_filter != "all":
            search_result = ConditionStatements.objects.search(query).filter(management_confirm=management_confirm_filter).all()

        elif accounting_confirm_filter != "all" and management_confirm_filter != "all":
            search_result = ConditionStatements.objects.search(query).filter(accounting_confirm=accounting_confirm_filter,
                                                                    management_confirm=management_confirm_filter).all()
        else:
            search_result = ConditionStatements.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:condition_statements_search'
        context['list_url'] = 'projects_docs:condition_statements'
        return context


# ConditionStatements - End

# -----------------------------------------------------


# RegisteredDocs - Start

class RegisteredDocsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/registered_docs_list.html'
    model = RegisteredDocs
    context_object_name = "registered_docs"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:registered_docs_search'
        context['create_url'] = 'projects_docs:registered_doc_create'
        context['persian_object_name'] = 'سند ثبتی'
        return context


class RegisteredDocsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegisteredDocs
    template_name = 'projects_docs/registered_doc_create_update.html'
    form_class = RegisteredDocsForm
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت ثبت شد"


class RegisteredDocsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RegisteredDocs
    template_name = 'projects_docs/registered_doc_create_update.html'
    form_class = RegisteredDocsForm
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت ویرایش شد"


class RegisteredDocsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:registered_docs")
    success_message = "سند ثبتی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        registered_doc = get_object_or_404(RegisteredDocs, pk=_id)
        return registered_doc


class RegisteredDocsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/registered_docs_list.html'
    model = RegisteredDocs
    context_object_name = "registered_docs"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        doc_type_filter = self.request.GET.get('doc_type')

        global search_result

        if doc_type_filter != "all":
            search_result = RegisteredDocs.objects.search(query).filter(doc_type=doc_type_filter).all()
        else:
            search_result = RegisteredDocs.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:registered_docs_search'
        context['list_url'] = 'projects_docs:registered_docs'
        return context


# RegisteredDocs - End

# -----------------------------------------------------


# OfficialDocs - Start

class OfficialDocsList(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/official_docs_list.html'
    model = OfficialDocs
    context_object_name = "official_docs"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects_docs:official_docs_search'
        context['create_url'] = 'projects_docs:official_doc_create'
        context['persian_object_name'] = 'سند اداری'
        return context


class OfficialDocsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            return super().form_invalid(form)
        elif doc_type == "lic" and license_type is None:
            form.add_error('license_type', 'لطفا نوع پروانه را انتخاب کنید')
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class OfficialDocsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
            return super().form_invalid(form)
        elif doc_type == "lic" and license_type is None:
            form.add_error('license_type', 'لطفا نوع پروانه را انتخاب کنید')
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class OfficialDocsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects_docs:official_docs")
    success_message = "سند اداری با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        official_doc = get_object_or_404(OfficialDocs, pk=_id)
        return official_doc


class OfficialDocsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects_docs/official_docs_list.html'
    model = OfficialDocs
    context_object_name = "official_docs"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        doc_type_filter = self.request.GET.get('doc_type')

        global search_result

        if doc_type_filter != "all" and doc_type_filter in ['let', 'lic', 'crt'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(doc_type=doc_type_filter).all()

        elif doc_type_filter != "all" and doc_type_filter in ['snd', 'rec'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(letter_type=doc_type_filter).all()

        elif doc_type_filter != "all" and doc_type_filter in ['des', 'con', 'dac', 'tci'] and date_filter == "all":
            search_result = OfficialDocs.objects.search(query).filter(license_type=doc_type_filter).all()

        elif doc_type_filter == "all" and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter)).all()

        elif doc_type_filter != "all" and doc_type_filter in ['let', 'lic', 'crt'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter),
                                                                    doc_type=doc_type_filter).all()
            
        elif doc_type_filter != "all" and doc_type_filter in ['snd', 'rec'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter),
                                                                    letter_type=doc_type_filter).all()
            
        elif doc_type_filter != "all" and doc_type_filter in ['des', 'con', 'dac', 'tci'] and date_filter != "all":
            search_result = OfficialDocs.objects.search(query).filter(send_receive_date__range=filter_date_values(date_filter),
                                                                    license_type=doc_type_filter).all()
        else:
            search_result = OfficialDocs.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects_docs:official_docs_search'
        context['list_url'] = 'projects_docs:official_docs'
        return context


# OfficialDocs - End

# -----------------------------------------------------




