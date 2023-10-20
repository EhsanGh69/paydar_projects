from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values, fund_validation, cash_box_validation
from .models import Cheques, Fund, ReceivePay, CashBox
from .forms import ChequesForm, FundForm, ReceivePayForm, CashBoxForm




# Cheques - Start

class ChequesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cheques'
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


class ChequesCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_cheques'
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


class ChequesUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_cheques'
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


class ChequesDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_cheques'
    success_url = reverse_lazy("cheques_receive_pay:cheques")
    success_message = "چک با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cheque = get_object_or_404(Cheques, pk=_id)
        return cheque
    

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
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        cheque_type_filter = self.request.GET.get('cheque_type')

        global search_result

        if cheque_type_filter != "all" and date_filter == "all":
            search_result = Cheques.objects.search(query).filter(cheque_type=cheque_type_filter).all() # type: ignore

        elif cheque_type_filter == "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__date__range=filter_date_values(date_filter)).all() # type: ignore

        elif cheque_type_filter != "all" and date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__date__range=filter_date_values(date_filter), cheque_type=cheque_type_filter).all() # type: ignore
        else:
            search_result = Cheques.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:cheques_search'
        context['list_url'] = 'cheques_receive_pay:cheques'
        context['query'] = query
        context['date_filter'] = date_filter
        context['cheque_type_filter'] = cheque_type_filter
        return context


# Cheques - End

# -----------------------------------------------

# Fund - Start

class FundList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_fund'
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Fund
    context_object_name = "funds"
    paginate_by = 9

    def get_queryset(self):
        return Fund.objects.order_by('full_name', '-operation_type', '-id').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['create_url'] = 'cheques_receive_pay:fund_create'
        context['persian_object_name'] = 'تنخواه'
        return context


class FundCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_fund'
    template_name = 'cheques_receive_pay/fund_create_update.html'
    model = Fund
    form_class = FundForm
    success_url = reverse_lazy("cheques_receive_pay:funds")
    success_message = "عملیات تنخواه با موفقیت ثبت شد"

    def get_form_kwargs(self):
        kwargs = super(FundCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    
    def form_valid(self, form):
        validation_result = fund_validation(form=form, model=Fund, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form)  # type: ignore
        else:
            return super().form_valid(form)
        

class FundUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_fund'
    template_name = 'cheques_receive_pay/fund_create_update.html'
    model = Fund
    form_class = FundForm
    success_url = reverse_lazy("cheques_receive_pay:funds")
    success_message = "عملیات تنخواه با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(FundUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    
    def form_valid(self, form):
        validation_result = fund_validation(form=form, model=Fund, url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)

    
class FundDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_fund'
    success_url = reverse_lazy("cheques_receive_pay:funds")
    success_message = "عملیات تنخواه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        fund = get_object_or_404(Fund, pk=_id)
        return fund
    

class FundSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_fund'
    template_name = 'cheques_receive_pay/funds_list.html'
    model = Cheques
    context_object_name = "funds"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global operation_type_filter
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        operation_type_filter = self.request.GET.get('operation_type')

        global search_result

        if operation_type_filter != "all" and date_filter == "all":
            search_result = Fund.objects.search(query).filter(operation_type=operation_type_filter).all() # type: ignore

        elif operation_type_filter == "all" and date_filter != "all":
            search_result = Fund.objects.search(query).filter(charge_date__date__range=filter_date_values(date_filter)).all() # type: ignore

        elif operation_type_filter != "all" and date_filter != "all":
            search_result = Fund.objects.search(query).filter(charge_date__date__range=filter_date_values(date_filter), operation_type=operation_type_filter).all() # type: ignore
        else:
            search_result = Fund.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:funds_search'
        context['list_url'] = 'cheques_receive_pay:funds'
        context['query'] = query
        context['date_filter'] = date_filter
        context['operation_type_filter'] = operation_type_filter
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:receive_pays_search'
        context['create_url'] = 'cheques_receive_pay:receive_pay_create'
        context['persian_object_name'] = 'دریافت / پرداخت'
        return context


class ReceivePayCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_receivepay'
    template_name = 'cheques_receive_pay/receive_pay_create_update.html'
    model = Cheques
    form_class = ReceivePayForm
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")
    success_message = "دریافت / پرداخت با موفقیت ثبت شد"

    def get_form_kwargs(self):
        kwargs = super(ReceivePayCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    

class ReceivePayUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_receivepay'
    template_name = 'cheques_receive_pay/receive_pay_create_update.html'
    model = Cheques
    form_class = ReceivePayForm
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")
    success_message = "دریافت / پرداخت با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(ReceivePayUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class ReceivePayDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_receivepay'
    success_url = reverse_lazy("cheques_receive_pay:receive_pays")
    success_message = "دریافت / پرداخت با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        receive_pay = get_object_or_404(ReceivePay, pk=_id)
        return receive_pay
    

class ReceivePaySearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_receivepay'
    template_name = 'cheques_receive_pay/receive_pays_list.html'
    model = Cheques
    context_object_name = "receive_pays"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result

        if date_filter != "all":
            search_result = Cheques.objects.search(query).filter(due_date__date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = Cheques.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:receive_pays_search'
        context['list_url'] = 'cheques_receive_pay:receive_pays'
        context['query'] = query
        context['date_filter'] = date_filter
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
        return CashBox.objects.order_by('-id').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'cheques_receive_pay:cash_boxes_search'
        context['create_url'] = 'cheques_receive_pay:cash_box_create'
        context['persian_object_name'] = 'صندوق'
        return context



class CashBoxCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cheques_receive_pay.add_cashbox'
    template_name = 'cheques_receive_pay/cash_box_create_update.html'
    model = CashBox
    form_class = CashBoxForm
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")
    success_message = "عملیات صندوق با موفقیت ثبت شد"

    def form_valid(self, form):
        validation_result = cash_box_validation(form=form, model=CashBox, 
                                                url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)
        

class CashBoxUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cheques_receive_pay.change_cashbox'
    template_name = 'cheques_receive_pay/cash_box_create_update.html'
    model = CashBox
    form_class = CashBoxForm
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")
    success_message = "عملیات صندوق با موفقیت ویرایش شد"

    def form_valid(self, form):
        validation_result = cash_box_validation(form=form, model=CashBox, 
                                                url_name=self.request.resolver_match.url_name)
        if not validation_result:
            return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)


class CashBoxDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cheques_receive_pay.delete_cashbox'
    success_url = reverse_lazy("cheques_receive_pay:cash_boxes")
    success_message = "عملیات صندوق با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cash_box = get_object_or_404(CashBox, pk=_id)
        return cash_box


class CashBoxSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cheques_receive_pay.view_cashbox'
    template_name = 'cheques_receive_pay/cash_boxes_list.html'
    model = CashBox
    context_object_name = "cash_boxes"
    paginate_by = 1

    def get_queryset(self):
        global not_found
        global operation_type_filter
        not_found = False
        operation_type_filter = self.request.GET.get('operation_type')

        global search_result

        if operation_type_filter != "all":
            search_result = CashBox.objects.filter(operation_type=operation_type_filter).all() # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'cheques_receive_pay:cash_boxes_search'
        context['list_url'] = 'cheques_receive_pay:cash_boxes'
        context['operation_type_filter'] = operation_type_filter
        return context

# CashBox - End