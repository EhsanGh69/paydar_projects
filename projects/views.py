from typing import Any, Optional
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .models import Owners, Project
from .forms import OwnerForm, ProjectForm



# Owners - Start

class OwnersList(LoginRequiredMixin, ListView):
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:owners_search'
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
    # model = Owners
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
    paginate_by = 9

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        if query is not None:
            search = Owners.objects.search(query)
            if search:
                return search
            else:
                not_found = True
        
        return Owners.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:owners_search'
        return context


# Owners - End

# ---------------------------------------------------------

class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = "projects"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:projects_search'
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
    paginate_by = 9

    def get_queryset(self):
        global not_found
        not_found = False
        request = self.request
        query = request.GET.get('data_search')
        if query is not None:
            search = Project.objects.search(query)
            if search:
                return search
            else:
                not_found = True
        
        return Project.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'projects:projects_search'
        return context

