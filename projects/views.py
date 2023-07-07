from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from utils.tools import filter_date_values
from .models import Owners, Project, WorkReference, Costs, PaymentsImages
from .forms import OwnerForm, ProjectForm, WorkReferenceForm, CostsForm, PaymentsImagesForm




@login_required
def charts(request):
    
    return render(request, 'projects/charts.html', )


# Owners - Start

class OwnersList(LoginRequiredMixin, ListView):
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:owners_search'
        context['create_url'] = 'projects:owner_create'
        context['persian_object_name'] = 'مالک'
        return context


class OwnerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت اضافه شد"


class OwnerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت ویرایش شد"


class OwnerDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        owner = get_object_or_404(Owners, pk=_id)
        return owner


class OwnerSearch(LoginRequiredMixin, ListView):
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        
        search = Owners.objects.search(query)
        if not search:
            not_found = True

        return search
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:owners_search'
        context['list_url'] = 'projects:owners'
        return context


# Owners - End

# ---------------------------------------------------------

# Project - Start

class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = "projects"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:projects_search'
        context['create_url'] = 'projects:project_create'
        context['persian_object_name'] = 'پروژه'
        return context


class ProjectCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'projects/project_create_update.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت اضافه شد"


class ProjectUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'projects/project_create_update.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت ویرایش شد"


class ProjectDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    # model = Project
    success_url = reverse_lazy("projects:projects")
    success_message = "پروژه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        project = get_object_or_404(Project, pk=_id)
        return project
    

class ProjectSearch(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        contract_filter = self.request.GET.get('contract_type')

        global search_result
        if filter != "all":
            search_result = Project.objects.search(query).filter(contract_type=contract_filter).all()
        else:
            search_result = Project.objects.search(query)

        if not search_result:
            not_found = True
            
        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:projects_search'
        context['list_url'] = 'projects:projects'
        return context


# Project - End

# ---------------------------------------------------------


# WorkReference - Start

class WorkReferenceList(LoginRequiredMixin, ListView):
    template_name = 'projects/work_references_list.html'
    model = WorkReference
    context_object_name = "work_references"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:work_references_search'
        context['create_url'] = 'projects:work_reference_create'
        context['persian_object_name'] = 'ارجاع کار'
        return context
    


class WorkReferenceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WorkReference
    template_name = 'projects/work_reference_create_update.html'
    form_class = WorkReferenceForm
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت ثبت گردید"

    def get_form_kwargs(self):
        kwargs = super(WorkReferenceCreate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs


class WorkReferenceUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WorkReference
    template_name = 'projects/work_reference_create_update.html'
    form_class = WorkReferenceForm
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت ویرایش شد"

    def get_form_kwargs(self):
        kwargs = super(WorkReferenceUpdate, self).get_form_kwargs()
        kwargs.update({
            'url_name': self.request.resolver_match.url_name
        })
        return kwargs
    

class WorkReferenceDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects:work_references")
    success_message = "ارجاع کار با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        work_reference = get_object_or_404(WorkReference, pk=_id)
        return work_reference
    

class WorkReferenceSearch(LoginRequiredMixin, ListView):
    template_name = 'projects/work_references_list.html'
    model = WorkReference
    context_object_name = "work_references"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        date_filter = self.request.GET.get('date_filter')

        global search_result
        if date_filter != "all":
            search_result = WorkReference.objects.search(query).filter(follow_date__date__range=filter_date_values(date_filter)).all()
        else:
            search_result = WorkReference.objects.search(query).all()

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:work_references_search'
        context['list_url'] = 'projects:work_references'
        return context


# WorkReference - End

# ----------------------------------------------------------

# Costs - Start

class CostsList(LoginRequiredMixin, ListView):
    template_name = 'projects/costs_list.html'
    model = Costs
    context_object_name = "costs"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:costs_search'
        context['create_url'] = 'projects:cost_create'
        context['persian_object_name'] = 'هزینه'
        return context


class CostsCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Costs
    template_name = 'projects/cost_create_update.html'
    form_class = CostsForm
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت ثبت گردید"


class CostsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Costs
    template_name = 'projects/cost_create_update.html'
    form_class = CostsForm
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت ویرایش شد"


class CostsDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects:costs")
    success_message = "هزینه با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        cost = get_object_or_404(Costs, pk=_id)
        return cost


class CostsSearch(LoginRequiredMixin, ListView):
    template_name = 'projects/costs_list.html'
    model = Costs
    context_object_name = "costs"

    def get_queryset(self):
        global not_found
        not_found = False
        query = self.request.GET.get('data_search')
        
        search_result = Costs.objects.search(query).all()

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:costs_search'
        context['list_url'] = 'projects:costs'
        return context


# Costs - End

# --------------------------------------------------------

# PaymentsImages - Start

class PaymentsImagesList(LoginRequiredMixin, ListView):
    template_name = 'projects/payments_images_list.html'
    model = PaymentsImages
    context_object_name = "payments_images"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:payments_images_search'
        context['create_url'] = 'projects:payments_image_create'
        context['persian_object_name'] = 'تصویر فیش پرداختی'
        return context
    

class PaymentsImagesCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PaymentsImages
    template_name = 'projects/payments_image_create_update.html'
    form_class = PaymentsImagesForm
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت ثبت گردید"


class PaymentsImagesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PaymentsImages
    template_name = 'projects/payments_image_create_update.html'
    form_class = PaymentsImagesForm
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت ویرایش شد"


class PaymentsImagesDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("projects:payments_images")
    success_message = "تصاویر فیش‌های پرداختی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        payments_image = get_object_or_404(PaymentsImages, pk=_id)
        return payments_image
    

class PaymentsImagesSearch(LoginRequiredMixin, ListView):
    template_name = 'projects/payments_images_list.html'
    model = PaymentsImages
    context_object_name = "payments_images"

    def get_queryset(self):
        global not_found
        not_found = False
        query = self.request.GET.get('data_search')
        
        search_result = PaymentsImages.objects.search(query).all()

        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:payments_images_search'
        context['list_url'] = 'projects:payments_images'
        return context


