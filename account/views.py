from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DeleteView, FormView, CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group, Permission

from utils.tools import valid_select_permissions
from utils.report_tools import date_query

from .models import User, Report
from .forms import AuthenticateForm, AddUserForm, UpdateUserForm, AddGroupForm, UpdateGroupForm, GetReportForm



class CustomLogin(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticateForm



# Users - Start


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

        other_users = User.objects.exclude(id=id)
        is_exits_username = other_users.filter(username=username).exists()
        is_exits_mobile_number = other_users.filter(mobile_number=mobile_number).exists()
        if is_exits_username:
            form.add_error('username', 'کاربری با نام کاربری وارد شده وجود دارد، لطفا نام کاربری دیگری وارد کنید')
            return super().form_invalid(form) # type: ignore
        elif is_exits_mobile_number:
            form.add_error('mobile_number', 'شماره همراه وارد شده از قبل وجود دارد، لطفا شماره همراه دیگری وارد کنید')
            return super().form_invalid(form) # type: ignore
                
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
        
        search_result = User.objects.search(query).all() # type: ignore
        
        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        context['search_url'] = 'account:users_search'
        context['list_url'] = 'account:users'
        return context


# Users - End

# ----------------------------------------------


# Group - Start


class GroupList(LoginRequiredMixin, ListView):
    template_name = 'account/groups_list.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persian_object_name'] = 'گروه دسترسی'
        return context


class CreateGroup(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'account/group_create_update.html'
    form_class = AddGroupForm
    success_url = reverse_lazy('account:groups')
    success_message = "گروه دسترسی جدید با موفقیت به سامانه اضافه گردید"
    
    def form_valid(self, form):
        group_name = form.cleaned_data.get('group_name')
        codenames = form.cleaned_data.get('permissions')
        group = Group.objects.create(name=group_name)

        for codename in codenames:
            permission = get_object_or_404(Permission, codename=codename)
            group.permissions.add(permission)

        return super().form_valid(form)


class UpdateGroup(LoginRequiredMixin, SuccessMessageMixin, FormView):
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
            return super().form_invalid(form) # type: ignore

        Group.objects.filter(pk=id).update(name=group_name)

        for group_permission in group_permissions:
            permission = get_object_or_404(Permission, codename=group_permission.codename)
            group.permissions.remove(permission)
        
        for codename in codenames:
            permission = get_object_or_404(Permission, codename=codename)
            group.permissions.add(permission)
        return super().form_valid(form)


class DeleteGroup(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("account:groups")
    success_message = "گروه دسترسی با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        group = get_object_or_404(Group, pk=_id)
        return group

# Group - End

# -----------------------------------------

# Report - Start

class ReportsHistory(LoginRequiredMixin, ListView):
    template_name = 'account/report_list.html'
    model = Report
    context_object_name = 'reports'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persian_object_name'] = 'گزارش'
        return context


class CreateReport(LoginRequiredMixin, CreateView):
    template_name = 'account/create_report.html'
    form_class = GetReportForm
    success_url = reverse_lazy('account:report_create')

    def form_valid(self, form, **kwargs):
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        report_type = form.cleaned_data.get('report_type')
        form_valid = date_query(date_from, date_to, True)
        is_exists_query = date_query(date_from, date_to, False, False, report_type).exists() # type: ignore
        if form_valid:
            if is_exists_query:
                # context['new_report'] = date_query(date_from, date_to, False, False, report_type)
                # context['record_count'] = date_query(date_from, date_to, False, False, report_type).count() # type: ignore
                return super().form_valid(form)
            else:
                form.errors['__all__'] = form.error_class(["برای بازه‌ی زمانی وارد شده هیچ اطلاعاتی ثبت نشده است."])
                return super().form_invalid(form)
        else:
            form.errors['__all__'] = form.error_class(["برای بازه‌ی زمانی وارد شده گزارشی از قبل موجود می‌باشد."])
            return super().form_invalid(form)


class ReportResult(LoginRequiredMixin, DetailView):
    template_name = 'account/report_result.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        report = get_object_or_404(Report, pk=pk)
        return report
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ReportDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("account:reports")
    success_message = "گزارش با موفقیت حذف شد"

    def get_object(self, queryset=None):
        _id = int(self.kwargs.get('pk'))
        report = get_object_or_404(Report, pk=_id)
        return report
    

class SearchReports(LoginRequiredMixin, ListView):
    template_name = 'account/report_list.html'
    model = Report
    context_object_name = "reports"

    def get_queryset(self):
        global not_found
        not_found = False
        global query
        query = self.request.GET.get('data_search')
        
        search_result = User.objects.search(query).all() # type: ignore
        
        if not search_result:
            not_found = True

        return search_result
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_found'] = not_found
        return context
      