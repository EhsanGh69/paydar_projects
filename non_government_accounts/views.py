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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:contractors_search'
        context['create_url'] = 'non_government_accounts:contractor_create'
        context['persian_object_name'] = 'پیمانکار'
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
        not_found = False
        query = self.request.GET.get('data_search')

        search_result = Contractors.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:contractors_search'
        context['list_url'] = 'non_government_accounts:contractors'
        context['query'] = query
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:suppliers_search'
        context['create_url'] = 'non_government_accounts:supplier_create'
        context['persian_object_name'] = 'تأمین کننده'
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

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:suppliers_search'
        context['list_url'] = 'non_government_accounts:suppliers'
        context['query'] = query
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:personnel_search'
        context['create_url'] = 'non_government_accounts:personnel_create'
        context['persian_object_name'] = 'شخص پرسنل'
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
        not_found = False
        query = self.request.GET.get('data_search')

        search_result = Personnel.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:personnel_search'
        context['list_url'] = 'non_government_accounts:personnel'
        context['query'] = query
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:partners_search'
        context['create_url'] = 'non_government_accounts:partner_create'
        context['persian_object_name'] = 'شریک'
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
        not_found = False
        query = self.request.GET.get('data_search')
        
        search_result = Partners.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:partners_search'
        context['list_url'] = 'non_government_accounts:partners'
        context['query'] = query
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:buyers_sellers_search'
        context['create_url'] = 'non_government_accounts:buyer_seller_create'
        context['persian_object_name'] = 'خریدار / فروشنده'
        return context


class BuyersSellersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_buyerssellers'
    model = BuyersSellers
    template_name = 'non_government_accounts/buyer_seller_create_update.html'
    form_class = BuyersSellersForm
    success_url = reverse_lazy("non_government_accounts:buyers_sellers")
    success_message = "خریدار / فروشنده با موفقیت اضافه شد"

    def get_form_kwargs(self):
        kwargs = super(BuyersSellersCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class BuyersSellersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_buyerssellers'
    model = BuyersSellers
    template_name = 'non_government_accounts/buyer_seller_create_update.html'
    form_class = BuyersSellersForm
    success_url = reverse_lazy("non_government_accounts:buyers_sellers")
    success_message = "خریدار / فروشنده با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(BuyersSellersUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


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
        global date_filter
        not_found = False
        query = self.request.GET.get('data_search')
        buyer_seller_filter = self.request.GET.get('buyer_seller')
        payment_order_filter = self.request.GET.get('payment_order')
        date_filter = self.request.GET.get('date_filter')
        
        global search_result
        
        if buyer_seller_filter != "all" and payment_order_filter == "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter != "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_order=payment_order_filter).all() # type: ignore

        elif buyer_seller_filter != "all" and payment_order_filter != "all" and date_filter == "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_order=payment_order_filter, buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter == "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter)).all() # type: ignore

        elif buyer_seller_filter != "all" and payment_order_filter == "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter), buyer_seller=buyer_seller_filter).all() # type: ignore

        elif buyer_seller_filter == "all" and payment_order_filter != "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter), payment_order=payment_order_filter).all() # type: ignore
        
        elif buyer_seller_filter != "all" and payment_order_filter != "all" and date_filter != "all":
            search_result = BuyersSellers.objects.search(query).filter(payment_date__date__range=filter_date_values(date_filter), payment_order=payment_order_filter, buyer_seller=buyer_seller_filter).all() # type: ignore
        
        else:
            search_result = BuyersSellers.objects.search(query) # type: ignore

        
        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:buyers_sellers_search'
        context['list_url'] = 'non_government_accounts:buyers_sellers'
        context['query'] = query
        context['buyer_seller_filter'] = buyer_seller_filter
        context['payment_order_filter'] = payment_order_filter
        context['date_filter'] = date_filter
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:orders_search'
        context['create_url'] = 'non_government_accounts:order_create'
        context['persian_object_name'] = 'سفارش'
        return context
    

class OrdersCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'non_government_accounts.add_orders'
    model = Orders
    template_name = 'non_government_accounts/order_create_update.html'
    form_class = OrdersForm
    success_url = reverse_lazy("non_government_accounts:orders")
    success_message = "سفارش با موفقیت ثبت شد"

    def get_form_kwargs(self):
        kwargs = super(OrdersCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class OrdersUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'non_government_accounts.change_orders'
    model = Orders
    template_name = 'non_government_accounts/order_create_update.html'
    form_class = OrdersForm
    success_url = reverse_lazy("non_government_accounts:orders")
    success_message = "سفارش با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(OrdersUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


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
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        order_result_filter = self.request.GET.get('order_result')
        order_image_filter = self.request.GET.get('order_image_type')

        global search_result
        
        if order_result_filter != "all" and order_image_filter == "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter != "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(sended_image_type=order_image_filter).all() # type: ignore

        elif order_result_filter != "all" and order_image_filter != "all" and date_filter == "all":
            search_result = Orders.objects.search(query).filter(sended_image_type=order_image_filter, order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter == "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__date__range=filter_date_values(date_filter)).all() # type: ignore

        elif order_result_filter != "all" and order_image_filter == "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__date__range=filter_date_values(date_filter), order_result=order_result_filter).all() # type: ignore

        elif order_result_filter == "all" and order_image_filter != "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__date__range=filter_date_values(date_filter), sended_image_type=order_image_filter).all() # type: ignore
        
        elif order_result_filter != "all" and order_image_filter != "all" and date_filter != "all":
            search_result = Orders.objects.search(query).filter(order_date__date__range=filter_date_values(date_filter), sended_image_type=order_image_filter, order_result=order_result_filter).all() # type: ignore
        else:
            search_result = Orders.objects.search(query) # type: ignore

        if not search_result:
            not_found = True

        return search_result
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:orders_search'
        context['list_url'] = 'non_government_accounts:orders'
        context['query'] = query
        context['date_filter'] = date_filter
        context['order_result_filter'] = order_result_filter
        context['order_image_filter'] = order_image_filter
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'non_government_accounts:conflict_orders_search'
        context['create_url'] = 'non_government_accounts:conflict_order_create'
        context['persian_object_name'] = 'مغایرت سفارش'
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

        return search_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'non_government_accounts:conflict_orders_search'
        context['list_url'] = 'non_government_accounts:conflict_orders'
        context['query'] = query
        context['conflict_type_filter'] = conflict_type_filter
        return context


# ConflictOrders - End

# ---------------------------------------------------
