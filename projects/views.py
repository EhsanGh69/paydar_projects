from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .models import Owners
from .forms import OwnerCreateForm





class OwnersList(LoginRequiredMixin, ListView):
    template_name = 'projects/owner_list.html'
    model = Owners
    context_object_name = "owners"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'projects:owners_search'
        return context


class OwnerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerCreateForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت اضافه شد"


class OwnerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'projects/owner_create_update.html'
    model = Owners
    form_class = OwnerCreateForm
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت ویرایش شد"


class OwnerDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'projects/confirm_delete.html'
    model = Owners
    success_url = reverse_lazy("projects:owners")
    success_message = "مالک با موفقیت حذف شد"


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

