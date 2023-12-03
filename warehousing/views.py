from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values, warehouse_export_validation

from .models import Stuff, MainWarehouseImport, MainWarehouseExport, UseCertificate, ProjectWarehouse
from .forms import StuffForm, MainWarehouseImportForm, MainWarehouseExportForm, UseCertificateForm, ProjectWarehouseForm



# Stuff - Start

class StuffList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_stuff'
    template_name = 'warehousing/stuffs_list.html'
    model = Stuff
    context_object_name = "stuffs"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        queryset = Stuff.objects.order_by('stuff_type').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Stuff.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:stuffs_search'
        context['create_url'] = 'warehousing:stuff_create'
        context['list_url'] = 'warehousing:stuffs'
        context['persian_object_name'] = 'کالا'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        return context
    

class StuffCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'warehousing.add_stuff'
    template_name = 'warehousing/stuff_create_update.html'
    model = Stuff
    form_class = StuffForm
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت اضافه شد"


class StuffUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'warehousing.change_stuff'
    template_name = 'warehousing/stuff_create_update.html'
    model = Stuff
    form_class = StuffForm
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت ویرایش شد"


class StuffDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'warehousing.delete_stuff'
    success_url = reverse_lazy('warehousing:stuffs')
    success_message = "کالا با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        stuff = get_object_or_404(Stuff, pk=_id)
        return stuff
    

class StuffSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_stuff'
    template_name = 'warehousing/stuffs_list.html'
    model = Stuff
    context_object_name = "stuffs"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        not_found = False
        query = self.request.GET.get('data_search')

        global search_result
        search_result = Stuff.objects.search(query)  # type: ignore

        if not search_result:
            not_found = True
        else:
            search_result = search_result.order_by('stuff_type').all()

        return search_result

    def get_context_data(self, **kwargs):
        records_count = search_result.count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:stuffs_search'
        context['list_url'] = 'warehousing:stuffs'
        context['list_filters'] = {'data_search': query}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        return context


# Stuff - End

# ---------------------------------------
    
# MainWarehouseImport - Start

class WarehouseImportList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_mainwarehouseimport'
    template_name = 'warehousing/warehouse_imports_list.html'
    model = MainWarehouseImport
    context_object_name = "warehouse_imports"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = MainWarehouseImport.objects.order_by(order_by).all()
        else:
            queryset = MainWarehouseImport.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = MainWarehouseImport.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:warehouse_imports_search'
        context['create_url'] = 'warehousing:warehouse_import_create'
        context['list_url'] = 'warehousing:warehouse_imports'
        context['persian_object_name'] = 'کالای افزوده شده به انبار'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = {'تأمین کننده': 'supplier__full_name',
                                   'نوع کالا': 'stuff_type__stuff_type', 'تحویل گیرنده': 'receiver__full_name',
                                   'تاریخ ورود کالا': '-import_date', 'پروژه کالای مرجوعی': 'project_returned__title'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class WarehouseImportCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'warehousing.add_mainwarehouseimport'
    model = MainWarehouseImport
    template_name = 'warehousing/warehouse_import_create_update.html'
    form_class = MainWarehouseImportForm
    success_url = reverse_lazy("warehousing:warehouse_imports")
    success_message = "کالا با موفقیت به انبار افزوده شد"
        
    
class WarehouseImportUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'warehousing.change_mainwarehouseimport'
    model = MainWarehouseImport
    template_name = 'warehousing/warehouse_import_create_update.html'
    form_class = MainWarehouseImportForm
    success_url = reverse_lazy("warehousing:warehouse_imports")
    success_message = "کالای انبار با موفقیت ویرایش شد"
    

class WarehouseImportDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'warehousing.delete_mainwarehouseimport'
    success_url = reverse_lazy('warehousing:warehouse_imports')
    success_message = "کالای انبار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        warehouse_import = get_object_or_404(MainWarehouseImport, pk=_id)
        return warehouse_import
    

class WarehouseImportSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_mainwarehouseimport'
    template_name = 'warehousing/warehouse_imports_list.html'
    model = MainWarehouseImport
    context_object_name = "warehouse_imports"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global is_returned_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')
        is_returned_filter = self.request.GET.get('is_returned')
        order_by = self.request.GET.get('order_by')

        global search_result
        if is_returned_filter != "all" and date_filter == "all":
            search_result = MainWarehouseImport.objects.search(query).filter(is_returned=bool(int(is_returned_filter))).all()   # type: ignore
        elif is_returned_filter == "all" and date_filter != "all":
            search_result = MainWarehouseImport.objects.search(query).filter(import_date__range=filter_date_values(date_filter)).all()  # type: ignore
        elif is_returned_filter != "all" and date_filter != "all":
            search_result = MainWarehouseImport.objects.search(query).filter(import_date__range=filter_date_values(date_filter), is_returned=bool(int(is_returned_filter))).all()  # type: ignore
        else:
            search_result = MainWarehouseImport.objects.search(query)  # type: ignore

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
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:warehouse_imports_search'
        context['list_url'] = 'warehousing:warehouse_imports'
        context['list_filters'] = {'data_search': query, 'date_filter': date_filter,'is_returned': is_returned_filter}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = {'تأمین کننده': 'supplier__full_name', 'نوع کالا': 'stuff_type__stuff_type', 
        'تحویل گیرنده': 'receiver__full_name', 'تاریخ ورود کالا': '-import_date', 'پروژه کالای مرجوعی': 'project_returned__title'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# MainWarehouseImport - End

# -----------------------------------------------

# MainWarehouseExport - Start

class WarehouseExportList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_mainwarehouseexport'
    template_name = 'warehousing/warehouse_exports_list.html'
    model = MainWarehouseExport
    context_object_name = "warehouse_exports"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = MainWarehouseExport.objects.order_by(order_by).all()
        else:
            queryset = MainWarehouseExport.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = MainWarehouseExport.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:warehouse_exports_search'
        context['create_url'] = 'warehousing:warehouse_export_create'
        context['list_url'] = 'warehousing:warehouse_exports'
        context['persian_object_name'] = 'کالای خارج شده از  انبار'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = {'نوع کالا': 'stuff_type__stuff_type','تحویل دهنده': 'deliverer__full_name',
        'پرسنل درخواست‌کننده': 'personnel__full_name','پیمانکار درخواست‌کننده': 'contractor__full_name',
        'پروژه': 'project__title','تاریخ خروج کالا': '-export_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class WarehouseExportCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'warehousing.add_mainwarehouseexport'
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
            return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        stuffs = Stuff.objects.order_by('stuff_type').all()
        context = super().get_context_data(**kwargs)
        context['stuffs'] = stuffs
        return context
        

class WarehouseExportUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'warehousing.change_mainwarehouseexport'
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
            return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        stuffs = Stuff.objects.order_by('stuff_type').all()
        context = super().get_context_data(**kwargs)
        context['stuffs'] = stuffs
        return context


class WarehouseExportDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'warehousing.delete_mainwarehouseexport'
    success_url = reverse_lazy('warehousing:warehouse_exports')
    success_message = "کالای خارج‌ شده از انبار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        warehouse_export = get_object_or_404(MainWarehouseExport, pk=_id)
        return warehouse_export


class WarehouseExportSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_mainwarehouseexport'
    template_name = 'warehousing/warehouse_exports_list.html'
    model = MainWarehouseExport
    context_object_name = "warehouse_exports"
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
            search_result = MainWarehouseExport.objects.search(query).filter(export_date__range=filter_date_values(date_filter)).all()  # type: ignore
        else:
            search_result = MainWarehouseExport.objects.search(query)  # type: ignore

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
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:warehouse_exports_search'
        context['list_url'] = 'warehousing:warehouse_exports'
        context['list_filters'] = {'data_search': query, 'date_filter': date_filter}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = {'نوع کالا': 'stuff_type__stuff_type','تحویل دهنده': 'deliverer__full_name',
        'پرسنل درخواست‌کننده': 'personnel__full_name','پیمانکار درخواست‌کننده': 'contractor__full_name',
        'پروژه': 'project__title','تاریخ خروج کالا': '-export_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# MainWarehouseExport - End

# -------------------------------------------------

# UseCertificate - Start

class UseCertificateList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_usecertificate'
    template_name = 'warehousing/use_certificates_list.html'
    model = UseCertificate
    context_object_name = "use_certificates"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = UseCertificate.objects.order_by(order_by).all()
        else:
            queryset = UseCertificate.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = UseCertificate.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:use_certificates_search'
        context['create_url'] = 'warehousing:use_certificate_create'
        context['list_url'] = 'warehousing:use_certificates'
        context['persian_object_name'] = 'گواهی مصرف کالا'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = {'نوع کالا': 'stuff_type__stuff_type','تاریخ شروع مصرف': '-start_using_date',
        'تاریخ پایان مصرف': '-finish_using_date','تاریخ ارجاع به انبار': '-return_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class UseCertificateCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'warehousing.add_usecertificate'
    template_name = 'warehousing/use_certificate_create_update.html'
    model = UseCertificate
    form_class = UseCertificateForm
    success_url = reverse_lazy("warehousing:use_certificates")
    success_message = "گواهی مصرف کالا با موفقیت ثبت شد"


class UseCertificateUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'warehousing.change_usecertificate'
    template_name = 'warehousing/use_certificate_create_update.html'
    model = UseCertificate
    form_class = UseCertificateForm
    success_url = reverse_lazy("warehousing:use_certificates")
    success_message = "گواهی مصرف کالا با موفقیت ویرایش شد"


class UseCertificateDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'warehousing.delete_usecertificate'
    success_url = reverse_lazy('warehousing:use_certificates')
    success_message = "گواهی مصرف کالا با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        use_certificate = get_object_or_404(UseCertificate, pk=_id)
        return use_certificate
    

class UseCertificateSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_usecertificate'
    template_name = 'warehousing/use_certificates_list.html'
    model = UseCertificate
    context_object_name = "use_certificates"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global stuff_state
        global return_to
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        stuff_state = self.request.GET.get('stuff_state')
        return_to = self.request.GET.get('return_to')
        order_by = self.request.GET.get('order_by')

        global search_result
        if return_to is None and stuff_state == "def":
            search_result = UseCertificate.objects.search(query).filter(is_deficient=True).all()  # type: ignore
        elif return_to is None and stuff_state == "exc":
            search_result = UseCertificate.objects.search(query).filter(is_excess=True).all()  # type: ignore
        elif return_to == "prw" and stuff_state is None:
            search_result = UseCertificate.objects.search(query).filter(returned_to='prw').all()  # type: ignore
        elif return_to == "maw" and stuff_state is None:
            search_result = UseCertificate.objects.search(query).filter(returned_to='maw').all()  # type: ignore
        else:
            search_result = UseCertificate.objects.search(query)  # type: ignore

        if not search_result:
            not_found = True
        elif order_by is not None and order_by != "none":
            search_result = search_result.order_by(order_by).all()
        else:
            search_result = search_result.order_by('-id').all()

        return search_result

    def get_context_data(self, **kwargs):
        records_count = UseCertificate.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:use_certificates_search'
        context['list_url'] = 'warehousing:use_certificates'
        context['list_filters'] = {'data_search': query, 'stuff_state': stuff_state, 'return_to': return_to}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = {'نوع کالا': 'stuff_type__stuff_type','تاریخ شروع مصرف': '-start_using_date',
        'تاریخ پایان مصرف': '-finish_using_date','تاریخ ارجاع به انبار': '-return_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# UseCertificate - End

# -------------------------------------------------

# ProjectWarehouse - Start

class ProjectWarehouseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_projectwarehouse'
    template_name = 'warehousing/project_warehouses_list.html'
    model = ProjectWarehouse
    context_object_name = "project_warehouses"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = ProjectWarehouse.objects.order_by(order_by).all()
        else:
            queryset = ProjectWarehouse.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = ProjectWarehouse.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'warehousing:project_warehouses_search'
        context['create_url'] = 'warehousing:project_warehouse_create'
        context['list_url'] = 'warehousing:project_warehouses'
        context['persian_object_name'] = 'انبار پروژه'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = {'پروژه': 'project__title','پرسنل درخواست‌کننده': 'personnel_apply__full_name',
        'پیمانکار درخواست‌کننده': 'contractor_apply__full_name','نوع کالا': 'stuff_type__stuff_type',
        'پرسنل تحویل‌گیرنده': 'personnel_delivery__full_name','پیمانکار تحویل‌گیرنده': 'contractor_delivery__full_name',
        'تاریخ ورود/خروج': '-export_import_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ProjectWarehouseCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'warehousing.add_projectwarehouse'
    template_name = 'warehousing/project_warehouse_create_update.html'
    model = ProjectWarehouse
    form_class = ProjectWarehouseForm
    success_url = reverse_lazy("warehousing:project_warehouses")
    success_message = "عملیات انبار پروژه با موفقیت ثبت شد"

    def form_valid(self, form):
        project = form.cleaned_data.get('project')
        stuff_type = form.cleaned_data.get('stuff_type')
        stuff_amount = form.cleaned_data.get('stuff_amount')
        status = form.cleaned_data.get('status')
        warehouse_export_check = MainWarehouseExport.objects.filter(project__title=project, 
        stuff_type=stuff_type, stuff_amount=stuff_amount).exists()

        if status == 'imp':
            if warehouse_export_check:
                return super().form_valid(form)
            else:
                form.errors['__all__'] = form.error_class(["پروژه، نوع کالا یا مقدار کالای وارد‌شده با اطلاعات موجود در لیست خروج از انبار اصلی مغایرت دارد"])
                return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)


class ProjectWarehouseUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'warehousing.change_projectwarehouse'
    template_name = 'warehousing/project_warehouse_create_update.html'
    model = ProjectWarehouse
    form_class = ProjectWarehouseForm
    success_url = reverse_lazy("warehousing:project_warehouses")
    success_message = "عملیات انبار پروژه با موفقیت ویرایش شد"

    def form_valid(self, form):
        project = form.cleaned_data.get('project')
        stuff_type = form.cleaned_data.get('stuff_type')
        stuff_amount = form.cleaned_data.get('stuff_amount')
        status = form.cleaned_data.get('status')
        warehouse_export_check = MainWarehouseExport.objects.filter(project__title=project, 
        stuff_type=stuff_type, stuff_amount=stuff_amount).exists()

        if status == 'imp':
            if warehouse_export_check:
                return super().form_valid(form)
            else:
                form.errors['__all__'] = form.error_class(["پروژه، نوع کالا یا مقدار کالای وارد‌شده با اطلاعات موجود در لیست خروج از انبار اصلی مغایرت دارد"])
                return super().form_invalid(form) # type: ignore
        else:
            return super().form_valid(form)


class ProjectWarehouseDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'warehousing.delete_projectwarehouse'
    success_url = reverse_lazy('warehousing:project_warehouses')
    success_message = "عملیات انبار پروژه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        project_warehouse = get_object_or_404(ProjectWarehouse, pk=_id)
        return project_warehouse


class ProjectWarehouseSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'warehousing.view_projectwarehouse'
    template_name = 'warehousing/project_warehouses_list.html'
    model = ProjectWarehouse
    context_object_name = "project_warehouses"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global stuff_status
        global date_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        stuff_status = self.request.GET.get('stuff_status')
        date_filter = self.request.GET.get('date_filter')
        order_by = self.request.GET.get('order_by')

        global search_result
        if date_filter != "all" and stuff_status == "all":
            search_result = ProjectWarehouse.objects.search(query).filter(export_import_date__range=filter_date_values(date_filter)).all()  # type: ignore
        elif date_filter == "all" and stuff_status != "all" and stuff_status == "exp":
            search_result = ProjectWarehouse.objects.search(query).filter(status="exp").all()  # type: ignore
        elif date_filter == "all" and stuff_status != "all" and stuff_status == "imp":
            search_result = ProjectWarehouse.objects.search(query).filter(status="imp").all()  # type: ignore
        elif date_filter != "all" and stuff_status != "all" and stuff_status == "exp":
            search_result = ProjectWarehouse.objects.search(query).filter(status="exp", export_import_date__range=filter_date_values(date_filter)).all()  # type: ignore
        elif date_filter != "all" and stuff_status != "all" and stuff_status == "imp":
            search_result = ProjectWarehouse.objects.search(query).filter(status="imp", export_import_date__range=filter_date_values(date_filter)).all()  # type: ignore
        else:
            search_result = ProjectWarehouse.objects.search(query)  # type: ignore

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
            self.paginate_by = int(record_number)  # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'warehousing:project_warehouses_search'
        context['list_url'] = 'warehousing:project_warehouses'
        context['list_filters'] = {'data_search': query, 'date_filter': date_filter,'stuff_status': stuff_status}
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = {'پروژه': 'project__title','پرسنل درخواست‌کننده': 'personnel_apply__full_name',
        'پیمانکار درخواست‌کننده': 'contractor_apply__full_name','نوع کالا': 'stuff_type__stuff_type',
        'پرسنل تحویل‌گیرنده': 'personnel_delivery__full_name','پیمانکار تحویل‌گیرنده': 'contractor_delivery__full_name',
        'تاریخ ورود/خروج': '-export_import_date'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# ProjectWarehouse - End
