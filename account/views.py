from os import name
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DeleteView, FormView
from django.contrib.auth.models import Group, Permission

from utils.tools import valid_select_permissions, password_validation

from .models import User
from .forms import (
    UserLogin, UserChangePassword, AddUserForm, UpdateUserForm, AddGroupForm, UpdateGroupForm, UserEditAccount
)



class Login(FormView):
    template_name = 'auth/login.html'
    form_class = UserLogin
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.errors['__all__'] = form.error_class(["نام کاربری یا رمز عبور اشتباه است"])
            return super().form_invalid(form)


def log_out(request):
    logout(request)
    return redirect('login')


class ChangePassword(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'auth/change_password.html'
    form_class = UserChangePassword
    success_url = reverse_lazy('index')
    success_message = "رمز عبور شما با موفقیت تغییر یافت"

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password')
        confirm_new_password = form.cleaned_data.get('confirm_new_password')
        check_old_password = check_password(old_password, user.password) # type: ignore
        validation_result = password_validation(new_password, user.username) # type: ignore
        if check_old_password and validation_result == 'not_err':
            user.set_password(new_password) # type: ignore
            user.save()
            update_session_auth_hash(self.request, user) # type: ignore
            return super().form_valid(form)
        elif not check_old_password:
            form.add_error('old_password', 'رمز عبور کنونی اشتباه وارد شده است')
            return super().form_invalid(form)
        elif len(new_password) < 8: # type: ignore
            form.add_error('new_password', 'رمز عبور باید حداقل هشت کاراکتر باشد')
            return super().form_invalid(form)
        elif validation_result == 'combine_err':
            form.add_error('new_password', 'رمز عبور باید ترکیبی از حروف و اعداد باشد')
            return super().form_invalid(form)
        elif validation_result == 'similar_err':
            form.add_error('new_password', 'رمز عبور نباید شبیه نام کاربری باشد')
            return super().form_invalid(form)
        elif new_password != confirm_new_password:
            form.add_error('confirm_new_password', 'تایید رمز عبور با رمز عبور یکسان نمی باشد')
            return super().form_invalid(form)


class EditAccount(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "auth/edit_account.html"
    form_class = UserEditAccount
    success_url = reverse_lazy('index')
    success_message = "مشخصات کاربری شما با موفقیت ویرایش شد"

    def get_initial(self):
        initial = super(EditAccount, self).get_initial()
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        initial.update({
            'mobile_number': user.mobile_number,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        return initial

    def form_valid(self, form):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        mobile_number = form.cleaned_data.get('mobile_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        other_users = User.objects.exclude(username=user.username)
        is_exits_mobile_number = other_users.filter(mobile_number=mobile_number).exists()
        if is_exits_mobile_number:
            form.add_error('mobile_number', 'شماره همراه وارد شده از قبل وجود دارد، لطفا شماره همراه دیگری وارد کنید')
            return super().form_invalid(form)

        User.objects.filter(username=user.username).update(mobile_number=mobile_number,first_name=first_name, 
        last_name=last_name)
                
        return super().form_valid(form)


#? Users - Start


class UsersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'account.view_user'
    template_name = 'account/users_list.html'
    model = User
    context_object_name = "users"
    paginate_by = 9

    def get_queryset(self):
        global queryset
        queryset = User.objects.order_by('-is_superuser', '-date_joined').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'account:users_search'
        context['create_url'] = 'account:user_create'
        context['records_count'] = queryset.count()
        context['record_number'] = 9
        context['persian_object_name'] = 'کاربر'
        return context
    

class CreateUser(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    permission_required = 'account.add_user'
    template_name = 'account/user_create_update.html'
    form_class = AddUserForm
    success_url = reverse_lazy('account:users')
    success_message = "کاربر جدید با موفقیت به سامانه اضافه گردید"
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = make_password(form.cleaned_data.get('password'))
        mobile_number = form.cleaned_data.get('mobile_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        access_group = form.cleaned_data.get('access_group')

        user = User.objects.create(username=username, password=password, mobile_number=mobile_number,
                                        first_name=first_name, last_name=last_name)
        group = get_object_or_404(Group, name=access_group)
        user.groups.add(group)
            

        return super().form_valid(form)
    

class UpdateUser(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    permission_required = 'account.change_user'
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
        context['user_group'] = user.groups.all()[0]
        return context
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=id)
        mobile_number = form.cleaned_data.get('mobile_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        access_group = form.cleaned_data.get('access_group')
        is_active = form.cleaned_data.get('is_active')
        user_groups = user.groups.all()

        other_users = User.objects.exclude(id=id)
        is_exits_username = other_users.filter(username=username).exists()
        is_exits_mobile_number = other_users.filter(mobile_number=mobile_number).exists()
        if is_exits_username:
            form.add_error('username', 'کاربری با نام کاربری وارد شده وجود دارد، لطفا نام کاربری دیگری وارد کنید')
            return super().form_invalid(form)
        elif is_exits_mobile_number:
            form.add_error('mobile_number', 'شماره همراه وارد شده از قبل وجود دارد، لطفا شماره همراه دیگری وارد کنید')
            return super().form_invalid(form) 
                
        if not is_active:
            User.objects.filter(pk=id).update(username=username, mobile_number=mobile_number,
                                                    first_name=first_name, last_name=last_name, is_active=False)
        else:
            User.objects.filter(pk=id).update(username=username, mobile_number=mobile_number,
                                                first_name=first_name, last_name=last_name, is_active=True)
        for user_group in user_groups:
            group = get_object_or_404(Group, name=user_group)
            user.groups.remove(group)
        
        new_group = get_object_or_404(Group, name=access_group)
        user.groups.add(new_group)
            
        return super().form_valid(form)
    

class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'account.delete_user'
    success_url = reverse_lazy("account:users")
    success_message = "کاربر با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=_id)
        return user
    

class SearchUsers(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'account.view_user'
    template_name = 'account/users_list.html'
    model = User
    context_object_name = "users"
    paginate_by = 9

    def get_queryset(self):
        global not_found
        global query
        global search_result
        not_found = False
        query = self.request.GET.get('data_search')
        
        search_result = User.objects.search(query).all()  # type: ignore
        
        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'account:users_search'
        context['list_url'] = 'account:users'
        context['query'] = query
        context['records_count'] = search_result.count()
        context['record_number'] = 9
        return context


# Users - End

# ----------------------------------------------

# Group - Start

class GroupList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'account.view_group'
    template_name = 'account/groups_list.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 4

    def get_queryset(self):
        global queryset
        queryset = Group.objects.order_by('name').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = 'account:groups_search'
        context['create_url'] = 'account:group_create'
        context['records_count'] = queryset.count()
        context['record_number'] = 4
        context['persian_object_name'] = 'گروه دسترسی'
        return context


class CreateGroup(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    permission_required = 'account.add_group'
    template_name = 'account/group_create_update.html'
    form_class = AddGroupForm
    success_url = reverse_lazy('account:groups')
    success_message = "گروه دسترسی جدید با موفقیت به سامانه اضافه گردید"
    
    def form_valid(self, form):
        group_name = form.cleaned_data.get('group_name')
        codenames = form.cleaned_data.get('permissions')
        group = Group.objects.create(name=group_name)

        for codename in codenames: # type: ignore
            permission = get_object_or_404(Permission, codename=codename)
            group.permissions.add(permission)

        return super().form_valid(form)


class UpdateGroup(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    permission_required = 'account.change_group'
    template_name = 'account/group_create_update.html'
    form_class = UpdateGroupForm
    success_url = reverse_lazy('account:groups')
    success_message = "گروه دسترسی با موفقیت ویرایش شد"

    def get_initial(self):
        initial = super(UpdateGroup, self).get_initial()
        id = int(self.kwargs.get('pk'))
        group = get_object_or_404(Group, pk=id)
        initial.update({
            'group_name': group.name
        })
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = int(self.kwargs.get('pk'))
        group = get_object_or_404(Group, pk=id)
        context['group_permissions'] = [permission.codename for permission in group.permissions.all()]
        context['valid_permissions'] = valid_select_permissions
        return context
    
    def form_valid(self, form):
        id = int(self.kwargs.get('pk'))
        group = get_object_or_404(Group, pk=id)
        group_name = form.cleaned_data.get('group_name')
        codenames = form.cleaned_data.get('permissions')
        group_permissions = group.permissions.all()

        other_groups = Group.objects.exclude(id=id)
        is_exits_group_name = other_groups.filter(name=group_name).exists()
        if is_exits_group_name:
            form.add_error('group_name', 'گروه دسترسی با این نام وجود دارد، لطفا نام دیگری وارد کنید')
            return super().form_invalid(form) 

        Group.objects.filter(pk=id).update(name=group_name)

        for group_permission in group_permissions:
            permission = get_object_or_404(Permission, codename=group_permission.codename)
            group.permissions.remove(permission)
        
        for codename in codenames: # type: ignore
            permission = get_object_or_404(Permission, codename=codename)
            group.permissions.add(permission)
        return super().form_valid(form)


class DeleteGroup(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'account.delete_group'
    success_url = reverse_lazy("account:groups")
    success_message = "گروه دسترسی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        group = get_object_or_404(Group, pk=_id)
        return group


class SearchGroups(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'account.view_group'
    template_name = 'account/groups_list.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 4

    def get_queryset(self):
        global not_found
        global query
        global search_result
        not_found = False
        query = self.request.GET.get('data_search')
        
        search_result = Group.objects.filter(name__icontains=query).distinct().all()
        
        if not search_result:
            not_found = True

        return search_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'account:groups_search'
        context['list_url'] = 'account:groups'
        context['query'] = query
        context['records_count'] = search_result.count()
        context['record_number'] = 4
        return context


# Group - End

# -----------------------------------------     