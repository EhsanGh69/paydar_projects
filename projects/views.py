from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from utils.tools import filter_date_values
from account.models import UserActionsLog
from .models import Owners, Project, WorkReference, Costs, PaymentsImages
from .forms import OwnerForm, ProjectForm, WorkReferenceForm, CostsForm, PaymentsImagesForm




@login_required
def charts(request):
    
    return render(request, 'projects/charts.html', )


# Owners - Start

class OwnersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_owners'
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Owners.objects.order_by(order_by).all()
        else:
            queryset = Owners.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Owners.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:owners_search'
        context['create_url'] = 'projects:owner_create'
        context['list_url'] = 'projects:owners'
        context['persian_object_name'] = 'مالک'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'نام و نام خانوادگی': 'full_name'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class OwnerCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects.add_owners'
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت اضافه شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="افزودن یک مالک جدید")
        return super().form_valid(form)


class OwnerUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects.change_owners'
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک مالک")
        return super().form_valid(form)


class OwnerDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects.delete_owners'
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        owner = get_object_or_404(Owners, pk=_id)
        return owner
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک مالک")
        return super().form_valid(form)


class OwnerSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_owners'
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        
        global search_result
        search_result = Owners.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects:owners_search'
        context['list_url'] = 'projects:owners'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'نام و نام خانوادگی': 'full_name'}
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Owners - End

# ---------------------------------------------------------

# Project - Start

class ProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_project'
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Project.objects.order_by(order_by).all()
        else:
            queryset = Project.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Project.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:projects_search'
        context['create_url'] = 'projects:project_create'
        context['list_url'] = 'projects:projects'
        context['persian_object_name'] = 'پروژه'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'عنوان پروژه': 'title', 'نوع قرارداد': 'contract_type' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects.add_project'
    template_name = 'projects/project_create_update.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت اضافه شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="افزودن یک پروژه جدید")
        return super().form_valid(form)


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects.change_project'
    template_name = 'projects/project_create_update.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک پروژه")
        return super().form_valid(form)


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects.delete_project'
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        project = get_object_or_404(Project, pk=_id)
        return project
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک پروژه")
        return super().form_valid(form)
    

class ProjectSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_project'
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global contract_filter
        global order_by
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        contract_filter = self.request.GET.get('contract_type')

        global search_result
        if contract_filter != "all":
            search_result = Project.objects.search(query).filter(contract_type=contract_filter).all() # type: ignore
        else:
            search_result = Project.objects.search(query) # type: ignore

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
        context['search_url'] = 'projects:projects_search'
        context['list_url'] = 'projects:projects'
        context['list_filters'] = { 'data_search': query, 'contract_type': contract_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'عنوان پروژه': 'title', 'نوع قرارداد': 'contract_type' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Project - End

# ---------------------------------------------------------


# WorkReference - Start

class WorkReferenceList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_workreference'
    template_name = 'projects/work_references_list.html'
    model = WorkReference
    context_object_name = "work_references"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = WorkReference.objects.order_by(order_by).all()
        else:
            queryset = WorkReference.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = WorkReference.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:work_references_search'
        context['create_url'] = 'projects:work_reference_create'
        context['list_url'] = 'projects:work_references'
        context['persian_object_name'] = 'ارجاع کار'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title', 'ارجاع دهنده': 'referrer', 
        'مأمور انجام': 'doing_agent', 'تاریخ پیگیری': '-follow_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class WorkReferenceCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects.add_workreference'
    model = WorkReference
    template_name = 'projects/work_reference_create_update.html'
    form_class = WorkReferenceForm
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت یک ارجاع کار جدید")
        return super().form_valid(form)


class WorkReferenceUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects.change_workreference'
    model = WorkReference
    template_name = 'projects/work_reference_create_update.html'
    form_class = WorkReferenceForm
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش یک ارجاع کار")
        return super().form_valid(form)
    

class WorkReferenceDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects.delete_workreference'
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        work_reference = get_object_or_404(WorkReference, pk=_id)
        return work_reference
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف یک ارجاع کار")
        return super().form_valid(form)
    

class WorkReferenceSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_workreference'
    template_name = 'projects/work_references_list.html'
    model = WorkReference
    context_object_name = "work_references"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global date_filter
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = WorkReference.objects.search(query).filter(follow_date__range=filter_date_values(date_filter)).all() # type: ignore
        else:
            search_result = WorkReference.objects.search(query).all() # type: ignore

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
        context['search_url'] = 'projects:work_references_search'
        context['list_url'] = 'projects:work_references'
        context['list_filters'] = { 'data_search': query, 'date_filter': date_filter }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title', 'ارجاع دهنده': 'referrer', 
        'مأمور انجام': 'doing_agent', 'تاریخ پیگیری': '-follow_date' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# WorkReference - End

# ----------------------------------------------------------

# Costs - Start

class CostsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_costs'
    template_name = 'projects/costs_list.html'
    model = Costs
    context_object_name = "costs"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = Costs.objects.order_by(order_by).all()
        else:
            queryset = Costs.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = Costs.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:costs_search'
        context['create_url'] = 'projects:cost_create'
        context['list_url'] = 'projects:costs'
        context['persian_object_name'] = 'هزینه'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


class CostsCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects.add_costs'
    model = Costs
    template_name = 'projects/cost_create_update.html'
    form_class = CostsForm
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت هزینه‌های جدید")
        return super().form_valid(form)


class CostsUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects.change_costs'
    model = Costs
    template_name = 'projects/cost_create_update.html'
    form_class = CostsForm
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="‌ویرایش هزینه‌ها")
        return super().form_valid(form)


class CostsDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects.delete_costs'
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cost = get_object_or_404(Costs, pk=_id)
        return cost
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف هزینه‌ها")
        return super().form_valid(form)


class CostsSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_costs'
    template_name = 'projects/costs_list.html'
    model = Costs
    context_object_name = "costs"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        
        global search_result
        search_result = Costs.objects.search(query).all() # type: ignore

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
        context['search_url'] = 'projects:costs_search'
        context['list_url'] = 'projects:costs'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context


# Costs - End

# --------------------------------------------------------

# PaymentsImages - Start

class PaymentsImagesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_paymentsimages'
    template_name = 'projects/payments_images_list.html'
    model = PaymentsImages
    context_object_name = "payments_images"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        global order_by
        order_by = self.request.GET.get('order_by')
        if order_by is not None and order_by != "none":
            queryset = PaymentsImages.objects.order_by(order_by).all()
        else:
            queryset = PaymentsImages.objects.order_by('-id').all()
        return queryset

    def get_context_data(self, **kwargs):
        records_count = PaymentsImages.objects.all().count()
        records_rows = list(range(1, records_count + 1))
        record_number = self.request.GET.get('record_number')
        if record_number:
            self.paginate_by = int(record_number) # type: ignore
        elif records_count > 9:
            record_number = 9
        else:
            record_number = records_count
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:payments_images_search'
        context['create_url'] = 'projects:payments_image_create'
        context['list_url'] = 'projects:payments_images'
        context['persian_object_name'] = 'تصویر فیش پرداختی'
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, queryset))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context
    

class PaymentsImagesCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'projects.add_paymentsimages'
    model = PaymentsImages
    template_name = 'projects/payments_image_create_update.html'
    form_class = PaymentsImagesForm
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت ثبت گردید"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content="ثبت تصاویر فیش‌های پرداختی جدید")
        return super().form_valid(form)


class PaymentsImagesUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'projects.change_paymentsimages'
    model = PaymentsImages
    template_name = 'projects/payments_image_create_update.html'
    form_class = PaymentsImagesForm
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت ویرایش شد"

    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="UP", log_content="ویرایش تصاویر فیش‌های پرداختی")
        return super().form_valid(form)


class PaymentsImagesDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'projects.delete_paymentsimages'
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        payments_image = get_object_or_404(PaymentsImages, pk=_id)
        return payments_image
    
    def form_valid(self, form):
        UserActionsLog.objects.create(user=self.request.user, log_type="DL", log_content="حذف تصاویر فیش‌های پرداختی")
        return super().form_valid(form)
    

class PaymentsImagesSearch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'projects.view_paymentsimages'
    template_name = 'projects/payments_images_list.html'
    model = PaymentsImages
    context_object_name = "payments_images"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global order_by
        not_found = False
        query = self.request.GET.get('data_search')
        
        global search_result
        search_result = PaymentsImages.objects.search(query).all() # type: ignore

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
        context['search_url'] = 'projects:payments_images_search'
        context['list_url'] = 'projects:payments_images'
        context['list_filters'] = { 'data_search': query }
        context['record_number'] = record_number
        context['records_count'] = records_count
        context['records_dict'] = dict(zip(records_rows, search_result))
        context['fields_order'] = { 'پروژه': 'project__title' }
        if order_by:
            context['order_by'] = order_by
        else:
            context['order_by'] = "none"
        return context

# PaymentsImages - End