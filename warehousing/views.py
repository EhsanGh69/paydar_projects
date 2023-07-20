from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.tools import filter_date_values

from .models import Stuff
from .forms import StuffForm



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
    








