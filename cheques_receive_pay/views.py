from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from utils.tools import filter_date_values, fund_rem_validation, fund_set_validation
from .models import Cheques, Fund
from .forms import ChequesForm, FundForm




# Cheques - Start

class ChequesList(LoginRequiredMixin, ListView):
    template_name = 'cheques_receive_pay/cheques_list.html'
    model = Cheques
    context_object_name = "cheques"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:cheques_search'
        context['create_url'] = 'cheques_receive_pay:cheque_create'
        context['persian_object_name'] = 'چک'
        return context


class ChequesCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cheques_receive_pay/cheque_create_update.html'
    model = Cheques
    form_class = ChequesForm
    success_url = reverse_lazy("cheques_receive_pay:cheques")
    success_message = "چک با موفقیت ثبت شد"

    def get_form_kwargs(self):
        kwargs = super(ChequesCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ChequesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cheques_receive_pay/cheque_create_update.html'
    model = Cheques
    form_class = ChequesForm
    success_url = reverse_lazy("cheques_receive_pay:cheques")
    success_message = "چک با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(ChequesUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ChequesDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("cheques_receive_pay:cheques")
    success_message = "چک با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cheque = get_object_or_404(Cheques, pk=_id)
        return cheque
    

class ChequesSearch(LoginRequiredMixin, ListView):
    template_name = 'cheques_receive_pay/cheques_list.html'
    model = Cheques
    context_object_name = "cheques"

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        cheque_type_filter = self.request.GET.get('cheque_type')

        global search_result

        if cheque_type_filter != "all" and date_filter == "all":
            search_result = Cheques.objects.search(query).filter(cheque_type=cheque_type_filter).all()

        elif cheque_type_filter == "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__date__range=filter_date_values(date_filter)).all()

        elif cheque_type_filter != "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__date__range=filter_date_values(date_filter), cheque_type=cheque_type_filter).all()
        else:
            search_result = Cheques.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:cheques_search'
        context['list_url'] = 'cheques_receive_pay:cheques'
        return context


# Cheques - End

# -----------------------------------------------

# Fund - Start

class FundList(LoginRequiredMixin, ListView):
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Fund
    context_object_name = "funds"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['create_url'] = 'cheques_receive_pay:fund_create'
        context['persian_object_name'] = 'تنخواه'
        return context


@login_required
def fund_create(request):
    fund_form = FundForm(request.POST or None)
    if fund_form.is_valid():
        full_name = fund_form.cleaned_data.get('full_name')
        operation_type = fund_form.cleaned_data.get('operation_type')
        if operation_type == 'rem':
            cost_amount = fund_form.cleaned_data.get('cost_amount')
            cost_description = fund_form.cleaned_data.get('cost_description')
            validation_result = fund_rem_validation(req=request, model=Fund, obj_id=False, name=full_name, form=fund_form,
                                                     cost=cost_amount, desc=cost_description)
            if validation_result:
                return HttpResponseRedirect("/cheques_receive_pay/funds")
        elif operation_type == 'set':
            charge_amount = fund_form.cleaned_data.get('charge_amount')
            charge_date = fund_form.cleaned_data.get('charge_date')
            validation_result = fund_set_validation(req=request, model=Fund, obj_id=False, name=full_name, form=fund_form,
                                                    charge=charge_amount, date=charge_date)
            if validation_result:
                return HttpResponseRedirect("/cheques_receive_pay/funds")
        else:
            fund_form = FundForm()
    return render(request, 'cheques_receive_pay/fund_create_update.html', {'form': fund_form})    
     

@login_required
def fund_update(request, *args, **kwargs):
    fund_id = kwargs['pk']
    fund = get_object_or_404(Fund, pk=fund_id)
    fund_form = FundForm(request.POST or None)

    if fund_form.is_valid():
        full_name = fund_form.cleaned_data.get('full_name')
        operation_type = fund_form.cleaned_data.get('operation_type')
        if operation_type == 'rem':
            cost_amount = fund_form.cleaned_data.get('cost_amount')
            cost_description = fund_form.cleaned_data.get('cost_description')
            validation_result = fund_rem_validation(req=request, model=Fund, obj_id=fund_id, obj=fund, name=full_name, form=fund_form,
                                                    cost=cost_amount, desc=cost_description)
            if validation_result:
                return HttpResponseRedirect("/cheques_receive_pay/funds")
        elif operation_type == 'set':
            charge_amount = fund_form.cleaned_data.get('charge_amount')
            charge_date = fund_form.cleaned_data.get('charge_date')
            validation_result = fund_set_validation(req=request, model=Fund, obj_id=fund_id, obj=fund, name=full_name, form=fund_form,
                                                    charge=charge_amount, date=charge_date)
            if validation_result:
                return HttpResponseRedirect("/cheques_receive_pay/funds")
    
    return render(request, 'cheques_receive_pay/fund_create_update.html', {'form': fund_form, 'fund': fund})

    

class FundDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("cheques_receive_pay:funds")
    success_message = "عملیات تنخواه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        fund = get_object_or_404(Fund, pk=_id)
        return fund
    

class FundSearch(LoginRequiredMixin, ListView):
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Cheques
    context_object_name = "funds"

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        operation_type_filter = self.request.GET.get('operation_type')

        global search_result

        if operation_type_filter != "all" and date_filter == "all":
            search_result = Fund.objects.search(query).filter(operation_type=operation_type_filter).all()

        elif operation_type_filter == "all" and date_filter != "all":
            search_result = Fund.objects.search(query).filter(charge_date__date__range=filter_date_values(date_filter)).all()

        elif operation_type_filter != "all" and date_filter != "all":
            search_result = Fund.objects.search(query).filter(charge_date__date__range=filter_date_values(date_filter), operation_type=operation_type_filter).all()
        else:
            search_result = Fund.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['list_url'] = 'cheques_receive_pay:funds'
        return context



