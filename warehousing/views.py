from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values, warehouse_export_validation

from .models import Stuff, MainWarehouseImport, MainWarehouseExport
from .forms import StuffForm, MainWarehouseImportForm, MainWarehouseExportForm



# Stuff - Start

class StuffList(LoginRequiredMixin, ListView):
    template_name = 'warehousing/stuffs_list.html'
    model = Stuff
    context_object_name = "stuffs"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:stuffs_search'
        context['create_url'] = 'warehousing:stuff_create'
        context['persian_object_name'] = 'کالا'
        return context
    

class StuffCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'warehousing/stuff_create_update.html'
    model = Stuff
    form_class = StuffForm
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت اضافه شد"


class StuffUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'warehousing/stuff_create_update.html'
    model = Stuff
    form_class = StuffForm
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت ویرایش شد"


class StuffDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        stuff = get_object_or_404(Stuff, pk=_id)
        return stuff


# Stuff - End

# ---------------------------------------
    
# MainWarehouseImport - Start

class WarehouseImportList(LoginRequiredMixin, ListView):
    template_name = 'warehousing/warehouse_imports_list.html'
    model = MainWarehouseImport
    context_object_name = "warehouse_imports"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:warehouse_imports_search'
        context['create_url'] = 'warehousing:warehouse_import_create'
        context['persian_object_name'] = 'کالای افزوده شده به انبار'
        return context


class WarehouseImportCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MainWarehouseImport
    template_name = 'warehousing/warehouse_import_create_update.html'
    form_class = MainWarehouseImportForm
    success_url = reverse_lazy("warehousing:warehouse_imports")
    success_message = "کالا با موفقیت به انبار افزوده شد"

    def get_form_kwargs(self):
        kwargs = super(WarehouseImportCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
        
    
class WarehouseImportUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MainWarehouseImport
    template_name = 'warehousing/warehouse_import_create_update.html'
    form_class = MainWarehouseImportForm
    success_url = reverse_lazy("warehousing:warehouse_imports")
    success_message = "کالای انبار با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(WarehouseImportUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    

class WarehouseImportDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('warehousing:warehouse_imports')
    success_message = "کالای انبار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        warehouse_import = get_object_or_404(MainWarehouseImport, pk=_id)
        return warehouse_import
    

class WarehouseImportSearch(LoginRequiredMixin, ListView):
    template_name = 'warehousing/warehouse_imports_list.html'
    model = MainWarehouseImport
    context_object_name = "warehouse_imports"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        is_returned_filter = self.request.GET.get('is_returned')

        global search_result

        if is_returned_filter != "all" and date_filter == "all":
            search_result = MainWarehouseImport.objects.search(query).filter(is_returned=bool(int(is_returned_filter))).all()
        elif is_returned_filter == "all" and date_filter != "all":
            search_result = MainWarehouseImport.objects.search(query).filter(date_time__date__range=filter_date_values(date_filter)).all()
        else:
            search_result = MainWarehouseImport.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:warehouse_imports_search'
        context['list_url'] = 'warehousing:warehouse_imports'
        return context


# MainWarehouseImport - End

# -----------------------------------------------

# MainWarehouseExport - Start

class WarehouseExportList(LoginRequiredMixin, ListView):
    template_name = 'warehousing/warehouse_exports_list.html'
    model = MainWarehouseExport
    context_object_name = "warehouse_exports"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:warehouse_exports_search'
        context['create_url'] = 'warehousing:warehouse_export_create'
        context['persian_object_name'] = 'کالای خارج شده از  انبار'
        return context
    

class WarehouseExportCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'warehousing/warehouse_export_create_update.html'
    model = MainWarehouseExport
    form_class = MainWarehouseExportForm
    success_url = reverse_lazy("warehousing:warehouse_exports")
    success_message = "خروج کالا از انبار با موفقیت ثبت شد"

    def form_valid(self, form):
        stuff_amount = form.cleaned_data.get('stuff_amount')
        stuff_type = form.cleaned_data.get('stuff_type')
        
        validation_result = warehouse_export_validation(imp_model=MainWarehouseImport, exp_model=MainWarehouseExport,
                                                        stuff_type=stuff_type, stuff_amount=stuff_amount, form=form)
            
        if not validation_result:
            return super().form_invalid(form)
        else:
            return super().form_valid(form)
        

class WarehouseExportUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'warehousing/warehouse_export_create_update.html'
    model = MainWarehouseExport
    form_class = MainWarehouseExportForm
    success_url = reverse_lazy("warehousing:warehouse_exports")
    success_message = "کالای خارج‌ شده از انبار با موفقیت ویرایش شد"

    def form_valid(self, form):
        stuff_amount = form.cleaned_data.get('stuff_amount')
        stuff_type = form.cleaned_data.get('stuff_type')
        validation_result = warehouse_export_validation(imp_model=MainWarehouseImport, exp_model=MainWarehouseExport,
                                                        stuff_type=stuff_type, stuff_amount=stuff_amount, form=form)
            
        if not validation_result:
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class WarehouseExportDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('warehousing:warehouse_exports')
    success_message = "کالای خارج‌ شده از انبار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        warehouse_export = get_object_or_404(MainWarehouseExport, pk=_id)
        return warehouse_export


class WarehouseExportSearch(LoginRequiredMixin, ListView):
    template_name = 'warehousing/warehouse_exports_list.html'
    model = MainWarehouseExport
    context_object_name = "warehouse_exports"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')

        search_result = MainWarehouseExport.objects.search(query)

        if not search_result:
            not_found = True

        return search_result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:warehouse_exports_search'
        context['list_url'] = 'warehousing:warehouse_exports'
        return context

# MainWarehouseExport - End

# -------------------------------------------------


