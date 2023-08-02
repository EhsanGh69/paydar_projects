from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values
from .models import Contracts
from .forms import ContractsForm




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