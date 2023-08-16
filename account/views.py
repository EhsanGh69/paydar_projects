from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group

from .models import User
from .forms import AuthenticateForm, AddUserForm, UpdateUserForm


class CustomLogin(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticateForm



class UsersList(LoginRequiredMixin, ListView):
    template_name = 'account/users_list.html'
    model = User
    context_object_name = "users"
    paginate_by = 9

    def get_queryset(self):
        return User.objects.order_by('-is_superuser', '-date_joined').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'account:users_search'
        context['create_url'] = 'account:user_create'
        context['persian_object_name'] = 'کاربر'
        return context
    

class CreateUser(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'account/user_create_update.html'
    form_class = AddUserForm
    success_url = reverse_lazy('account:users')
    success_message = "کاربر جدید با موفقیت به سامانه اضافه گردید"
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        mobile_number = form.cleaned_data.get('mobile_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        access_groups = form.cleaned_data.get('access_groups')
        user = User.objects.create(username=username, password=password, mobile_number=mobile_number,
                                    first_name=first_name, last_name=last_name)
        
        for access_group in access_groups:
            group = get_object_or_404(Group, name=access_group)
            user.groups.add(group)

        return super().form_valid(form)
    


class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'account/user_create_update.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('account:users')
    success_message = "کاربر با موفقیت ویرایش شد"

    def get_initial(self):
        initial = super(UpdateUser, self).get_initial()
        id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=id)
        initial.update({
            'username': user.username,
            'mobile_number': user.mobile_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active
        })
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=id)
        context['user'] = user
        context['user_groups'] = user.groups.all()
        context['all_groups'] = Group.objects.all()
        return context
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=id)
        mobile_number = form.cleaned_data.get('mobile_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        access_groups = form.cleaned_data.get('access_groups')
        is_active = form.cleaned_data.get('is_active')
        user_groups = user.groups.all()
        
        if not is_active:
            User.objects.filter(pk=id).update(username=username, mobile_number=mobile_number,
                                                    first_name=first_name, last_name=last_name, is_active=False)
        else:
            User.objects.filter(pk=id).update(username=username, mobile_number=mobile_number,
                                                first_name=first_name, last_name=last_name, is_active=True)
        for user_group in user_groups:
            group = get_object_or_404(Group, name=user_group)
            user.groups.remove(group)
        
        for access_group in access_groups:
            group = get_object_or_404(Group, name=access_group)
            user.groups.add(group)
        return super().form_valid(form)
    

class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("account:users")
    success_message = "کاربر با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=_id)
        return user
    

class SearchUsers(LoginRequiredMixin, ListView):
    template_name = 'account/users_list.html'
    model = User
    context_object_name = "users"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        
        search_result = User.objects.search(query).all()
        
        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'account:users_search'
        context['list_url'] = 'account:users'
        return context
    