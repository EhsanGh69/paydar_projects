from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values
from .models import Contractors, Suppliers, Personnel, Partners, BuyersSellers, Orders, ConflictOrders
from .forms import ContractorForm, SupplierForm, PersonnelForm, PartnersForm, BuyersSellersForm, OrdersForm, ConflictOrdersForm


# Contractors - Start

class ContractorsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_contractors'
    template_name = 'non_government_accounts/contractors_list.html'
    model = Contractors
    context_object_name = "contractors"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Contractors.objects.order_by(order_by).all()
        else:
            queryset = Contractors.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Contractors.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:contractors_search'
        context['create_url'] = 'non_government_accounts:contractor_create'
        context['list_url'] = 'non_government_accounts:contractors'
        context['persian_object_name'] = 'پیمانکار'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name', 
        'رشته شغلی': 'job'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ContractorCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_contractors'
    model = Contractors
    template_name = 'non_government_accounts/contractor_create_update.html'
    form_class = ContractorForm
    success_url = reverse_lazy("non_government_accounts:contractors")
    success_message = "پیمانکار با موفقیت اضافه شد"


class ContractorUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_contractors'
    model = Contractors
    template_name = 'non_government_accounts/contractor_create_update.html'
    form_class = ContractorForm
    success_url = reverse_lazy("non_government_accounts:contractors")
    success_message = "پیمانکار با موفقیت ویرایش شد"


class ContractorDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_contractors'
    success_url = reverse_lazy("non_government_accounts:contractors")
    success_message = "پیمانکار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        contractor = get_object_or_404(Contractors, pk=_id)
        return contractor
    

class ContractorSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_contractors'
    template_name = 'non_government_accounts/contractors_list.html'
    model = Contractors
    context_object_name = "contractors"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        order_by = self.request.GET.get('order_by')

        search_result = Contractors.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:contractors_search'
        context['list_url'] = 'non_government_accounts:contractors'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name', 
        'رشته شغلی': 'job'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# Contractors - End

# -----------------------------------------------

# Suppliers - Start

class SuppliersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_suppliers'
    template_name = 'non_government_accounts/suppliers_list.html'
    model = Suppliers
    context_object_name = "suppliers"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Suppliers.objects.order_by(order_by).all()
        else:
            queryset = Suppliers.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Suppliers.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:suppliers_search'
        context['create_url'] = 'non_government_accounts:supplier_create'
        context['list_url'] = 'non_government_accounts:suppliers'
        context['persian_object_name'] = 'تأمین کننده'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name', 
        'رشته شغلی': 'job'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class SupplierCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_suppliers'
    model = Suppliers
    template_name = 'non_government_accounts/supplier_create_update.html'
    form_class = SupplierForm
    success_url = reverse_lazy("non_government_accounts:suppliers")
    success_message = "تأمین کننده با موفقیت اضافه شد"


class SupplierUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_suppliers'
    model = Suppliers
    template_name = 'non_government_accounts/supplier_create_update.html'
    form_class = SupplierForm
    success_url = reverse_lazy("non_government_accounts:suppliers")
    success_message = "تأمین کننده با موفقیت ویرایش شد"


class SupplierDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_suppliers'
    success_url = reverse_lazy("non_government_accounts:suppliers")
    success_message = "تأمین کننده با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        supplier = get_object_or_404(Suppliers, pk=_id)
        return supplier
    

class SupplierSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_suppliers'
    template_name = 'non_government_accounts/suppliers_list.html'
    model = Suppliers
    context_object_name = "suppliers"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        not_found = False
        query = self.request.GET.get('data_search')

        search_result = Suppliers.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:suppliers_search'
        context['list_url'] = 'non_government_accounts:suppliers'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name', 
        'رشته شغلی': 'job'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    
# Suppliers - End

# ----------------------------------------------------

# Personnel - Start

class PersonnelList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_personnel'
    template_name = 'non_government_accounts/personnel_list.html'
    model = Personnel
    context_object_name = "personnel"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Personnel.objects.order_by(order_by).all()
        else:
            queryset = Personnel.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Personnel.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:personnel_search'
        context['create_url'] = 'non_government_accounts:personnel_create'
        context['list_url'] = 'non_government_accounts:personnel'
        context['persian_object_name'] = 'شخص پرسنل'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'نام و نام خانوادگی': 'full_name', 'رشته شغلی': 'job' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class PersonnelCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_personnel'
    model = Personnel
    template_name = 'non_government_accounts/personnel_create_update.html'
    form_class = PersonnelForm
    success_url = reverse_lazy("non_government_accounts:personnel")
    success_message = "شخص با موفقیت به پرسنل اضافه شد"


class PersonnelUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_personnel'
    model = Personnel
    template_name = 'non_government_accounts/personnel_create_update.html'
    form_class = PersonnelForm
    success_url = reverse_lazy("non_government_accounts:personnel")
    success_message = "شخص پرسنل با موفقیت ویرایش شد"


class PersonnelDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_personnel'
    success_url = reverse_lazy("non_government_accounts:personnel")
    success_message = "شخص پرسنل با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        person = get_object_or_404(Personnel, pk=_id)
        return person
    

class PersonnelSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_personnel'
    template_name = 'non_government_accounts/personnel_list.html'
    model = Personnel
    context_object_name = "personnel"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        order_by = self.request.GET.get('order_by')

        search_result = Personnel.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:personnel_search'
        context['list_url'] = 'non_government_accounts:personnel'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'نام و نام خانوادگی': 'full_name', 'رشته شغلی': 'job' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# Personnel - End

# --------------------------------------------------

# Partners - Start

class PartnersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_partners'
    template_name = 'non_government_accounts/partners_list.html'
    model = Partners
    context_object_name = "partners"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Partners.objects.order_by(order_by).all()
        else:
            queryset = Partners.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Partners.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:partners_search'
        context['create_url'] = 'non_government_accounts:partner_create'
        context['list_url'] = 'non_government_accounts:partners'
        context['persian_object_name'] = 'شریک'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class PartnersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_partners'
    model = Partners
    template_name = 'non_government_accounts/partner_create_update.html'
    form_class = PartnersForm
    success_url = reverse_lazy("non_government_accounts:partners")
    success_message = "شریک با موفقیت اضافه شد"


class PartnersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_partners'
    model = Partners
    template_name = 'non_government_accounts/partner_create_update.html'
    form_class = PartnersForm
    success_url = reverse_lazy("non_government_accounts:partners")
    success_message = "شریک با موفقیت ویرایش شد"


class PartnersDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_partners'
    success_url = reverse_lazy("non_government_accounts:partners")
    success_message = "شریک با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        partner = get_object_or_404(Partners, pk=_id)
        return partner
    

class PartnerSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_partners'
    template_name = 'non_government_accounts/partners_list.html'
    model = Partners
    context_object_name = "partners"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        order_by = self.request.GET.get('order_by')
        
        search_result = Partners.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:partners_search'
        context['list_url'] = 'non_government_accounts:partners'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    
# Partners - End

# ---------------------------------------------------

# BuyersSellers - Start

class BuyersSellersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_buyerssellers'
    template_name = 'non_government_accounts/buyers_sellers_list.html'
    model = BuyersSellers
    context_object_name = "buyers_sellers"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = BuyersSellers.objects.order_by(order_by).all()
        else:
            queryset = BuyersSellers.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = BuyersSellers.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:buyers_sellers_search'
        context['create_url'] = 'non_government_accounts:buyer_seller_create'
        context['list_url'] = 'non_government_accounts:buyers_sellers'
        context['persian_object_name'] = 'خریدار / فروشنده'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name',
        'تاریخ پرداخت': '-payment_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class BuyersSellersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_buyerssellers'
    model = BuyersSellers
    template_name = 'non_government_accounts/buyer_seller_create_update.html'
    form_class = BuyersSellersForm
    success_url = reverse_lazy("non_government_accounts:buyers_sellers")
    success_message = "خریدار / فروشنده با موفقیت اضافه شد"


class BuyersSellersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_buyerssellers'
    model = BuyersSellers
    template_name = 'non_government_accounts/buyer_seller_create_update.html'
    form_class = BuyersSellersForm
    success_url = reverse_lazy("non_government_accounts:buyers_sellers")
    success_message = "خریدار / فروشنده با موفقیت ویرایش شد"


class BuyersSellersDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_buyerssellers'
    success_url = reverse_lazy("non_government_accounts:buyers_sellers")
    success_message = "خریدار / فروشنده با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        buyer_seller = get_object_or_404(BuyersSellers, pk=_id)
        return buyer_seller


class BuyersSellersSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_buyerssellers'
    template_name = 'non_government_accounts/buyers_sellers_list.html'
    model = BuyersSellers
    context_object_name = "buyers_sellers"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global buyer_seller_filter
        global payment_order_filter
        global order_by
        global date_filter
        not_found = False
        query = self.request.GET.get('data_search')
        buyer_seller_filter = self.request.GET.get('buyer_seller')
        payment_order_filter = self.request.GET.get('payment_order')
        date_filter = self.request.GET.get('date_filter')
        order_by = self.request.GET.get('order_by')
        
        global search_result
        
        if buyer_seller_filter != "all" and payment_order_filter == "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter != "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_order=payment_order_filter).all() # type: ignore

        elif buyer_seller_filter != "all" and payment_order_filter != "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_order=payment_order_filter, buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter == "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif buyer_seller_filter != "all" and payment_order_filter == "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__range=filter_date_values(date_filter), buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter != "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__range=filter_date_values(date_filter), payment_order=payment_order_filter).all() # type: ignore
        
        elif buyer_seller_filter != "all" and payment_order_filter != "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__range=filter_date_values(date_filter), payment_order=payment_order_filter, buyer_seller=buyer_seller_filter).all() # type: ignore
        
        else:
            search_result = BuyersSellers.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:buyers_sellers_search'
        context['list_url'] = 'non_government_accounts:buyers_sellers'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'payment_order': payment_order_filter, 'buyer_seller': buyer_seller_filter}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'نام و نام خانوادگی': 'full_name',
        'تاریخ پرداخت': '-payment_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# BuyersSellers - Start

# --------------------------------------------------

# Orders - Start

class OrdersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_orders'
    template_name = 'non_government_accounts/orders_list.html'
    model = Orders
    context_object_name = "orders"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Orders.objects.order_by(order_by).all()
        else:
            queryset = Orders.objects.order_by('-id').all()
        return queryset
    
    def get_context_data(self, **kwargs):
        records_count = Orders.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:orders_search'
        context['create_url'] = 'non_government_accounts:order_create'
        context['list_url'] = 'non_government_accounts:orders'
        context['persian_object_name'] = 'سفارش'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'تأمین کننده': 'supplier__full_name', 
        'نوع سفارش': 'order_type', 'تاریخ سفارش': '-order_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class OrdersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_orders'
    model = Orders
    template_name = 'non_government_accounts/order_create_update.html'
    form_class = OrdersForm
    success_url = reverse_lazy("non_government_accounts:orders")
    success_message = "سفارش با موفقیت ثبت شد"


class OrdersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_orders'
    model = Orders
    template_name = 'non_government_accounts/order_create_update.html'
    form_class = OrdersForm
    success_url = reverse_lazy("non_government_accounts:orders")
    success_message = "سفارش با موفقیت ویرایش شد"


class OrdersDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_orders'
    success_url = reverse_lazy("non_government_accounts:orders")
    success_message = "سفارش با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        order = get_object_or_404(Orders, pk=_id)
        return order


class OrdersSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_orders'
    template_name = 'non_government_accounts/orders_list.html'
    model = Orders
    context_object_name = "orders"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global order_result_filter
        global order_image_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        order_result_filter = self.request.GET.get('order_result')
        order_image_filter = self.request.GET.get('order_image_type')
        order_by = self.request.GET.get('order_by')

        global search_result
        
        if order_result_filter != "all" and order_image_filter == "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter != "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(sended_image_type=order_image_filter).all() # type: ignore

        elif order_result_filter != "all" and order_image_filter != "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(sended_image_type=order_image_filter, order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter == "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__range=filter_date_values(date_filter)).all() # type: ignore

        elif order_result_filter != "all" and order_image_filter == "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__range=filter_date_values(date_filter), order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter != "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__range=filter_date_values(date_filter), sended_image_type=order_image_filter).all() # type: ignore
        
        elif order_result_filter != "all" and order_image_filter != "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__range=filter_date_values(date_filter), sended_image_type=order_image_filter, order_result=order_result_filter).all() # type: ignore
        else:
            search_result = Orders.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:orders_search'
        context['list_url'] = 'non_government_accounts:orders'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter, 
        'order_result': order_result_filter, 'order_image_type': order_image_filter}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'تأمین کننده': 'supplier__full_name', 
        'نوع سفارش': 'order_type', 'تاریخ سفارش': '-order_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Orders - End

# --------------------------------------------------

# ConflictOrders - Start

class ConflictOrdersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_conflictorders'
    template_name = 'non_government_accounts/conflict_orders_list.html'
    model = ConflictOrders
    context_object_name = "conflict_orders"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = ConflictOrders.objects.order_by(order_by).all()
        else:
            queryset = ConflictOrders.objects.order_by('-id').all()
        return queryset
    
    def get_context_data(self, **kwargs):
        records_count = ConflictOrders.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:conflict_orders_search'
        context['create_url'] = 'non_government_accounts:conflict_order_create'
        context['list_url'] = 'non_government_accounts:conflict_orders'
        context['persian_object_name'] = 'مغایرت سفارش'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'order__project__title', 'تأمین‌کننده': 'order__supplier__full_name',
        'نوع سفارش': 'order__order_type', 'تاریخ سفارش': '-order__order_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ConflictOrdersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_conflictorders'
    model = ConflictOrders
    template_name = 'non_government_accounts/conflict_order_create_update.html'
    form_class = ConflictOrdersForm
    success_url = reverse_lazy("non_government_accounts:conflict_orders")
    success_message = "مغایرت سفارش با موفقیت ثبت شد"


class ConflictOrdersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_conflictorders'
    model = ConflictOrders
    template_name = 'non_government_accounts/conflict_order_create_update.html'
    form_class = ConflictOrdersForm
    success_url = reverse_lazy("non_government_accounts:conflict_orders")
    success_message = "مغایرت سفارش با موفقیت ویرایش شد"


class ConflictOrdersDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'non_government_accounts.delete_conflictorders'
    success_url = reverse_lazy("non_government_accounts:conflict_orders")
    success_message = "مغایرت سفارش با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        conflict_order = get_object_or_404(ConflictOrders, pk=_id)
        return conflict_order


class ConflictOrdersSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'non_government_accounts.view_conflictorders'
    template_name = 'non_government_accounts/conflict_orders_list.html'
    model = ConflictOrders
    context_object_name = "conflict_orders"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global conflict_type_filter
        not_found = False
        query = self.request.GET.get('data_search')
        conflict_type_filter = self.request.GET.get('conflict_type')

        global search_result
        
        if conflict_type_filter != "all":
            search_result = ConflictOrders.objects.search(query).filter(conflict_type=conflict_type_filter).all() # type: ignore
        else:
            search_result = ConflictOrders.objects.search(query) # type: ignore

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
        context['search_url'] = 'non_government_accounts:conflict_orders_search'
        context['list_url'] = 'non_government_accounts:conflict_orders'
        context['list_filters'] = { 'data_search': query, 'conflict_type': conflict_type_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'order__project__title', 'تأمین‌کننده': 'order__supplier__full_name',
        'نوع سفارش': 'order__order_type', 'تاریخ سفارش': '-order__order_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# ConflictOrders - End

# ---------------------------------------------------