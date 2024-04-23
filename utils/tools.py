from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.conf import settings

from jdatetime import JalaliToGregorian, datetime

from account.models import User
from non_government_accounts.models import BuyersSellers
from projects.models import Project
from projects.templatetags.projects_tags import total_project_costs
from user_messages.models import Message



def translate_permissions_names(name):
    permission_translate = [_(w).replace('Can', '').replace('add', 'افزودن').replace('change', 'ویرایش').replace('delete', 'حذف').replace('view', 'مشاهده') for w in (name).split()]
    return ' '.join(permission_translate)


invalid_codenames = [
    'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
    'add_permission', 'change_permission', 'delete_permission', 'view_permission',
    'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
    'add_session', 'change_session', 'delete_session', 'view_session',
    'add_user', 'change_user', 'delete_user', 'view_user',
    'add_group', 'change_group', 'delete_group', 'view_group',
    'add_report', 'change_report', 'delete_report', 'view_report',
    'add_message', 'change_message', 'delete_message', 'view_message',
    'add_useractionslog', 'change_useractionslog', 'delete_useractionslog', 'view_useractionslog',
]

valid_select_permissions = [
    (permission.codename, translate_permissions_names(permission.name)) 
    for permission in Permission.objects.order_by('name').all() 
    if permission.codename not in invalid_codenames
] 


# source: https://www.appsloveworld.com/django/100/4/how-to-get-the-list-of-the-authenticated-users
def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


def password_validation(password, username):
    nums = [str(num) for num in range(0, 10)]
    list_control = []
    chars = {'.', '-', '_', '@'}
    username_letters = set(username.lower()) - chars
    password_letters = set(password.lower()) - chars
    for char in password:
        if char in nums:
            list_control.append('n')
        else:
            list_control.append('l')
    # checking password combination
    if 'n' not in list_control or 'l' not in list_control:
        return 'combine_err'
    # checking password similarity to username
    elif username_letters.intersection(password_letters) == username_letters:
        return 'similar_err'
    else:
        return 'not_err' 


def none_numeric_value(value):
    try:
        is_numeric = type(int(value)) is int
    except Exception:
        return True
    
    if is_numeric :
            raise ValidationError("مقدار این فیلد نمی‌تواند عددی می‌باشد", params={"value": value})
    

def image_size_validation(form, fields):
    size_valid = True
    for field in fields:
        file_field = form.cleaned_data.get(field)
        if file_field and file_field.size > settings.MAX_UPLOAD_SIZE:
            form.add_error(field, 'حجم تصویر بیش از حد مجاز است')
            size_valid = False

    return size_valid


def fund_validation(**kwargs):
    fund_valid = True
    full_name = kwargs['form'].cleaned_data.get('full_name')
    operation_type = kwargs['form'].cleaned_data.get('operation_type')
    if operation_type == 'rem':
        cost_amount = kwargs['form'].cleaned_data.get('cost_amount')
        cost_description = kwargs['form'].cleaned_data.get('cost_description')
        # receipt_image = kwargs['form'].cleaned_data.get('receipt_image')
        removal_date = kwargs['form'].cleaned_data.get('removal_date')
        fund_person = kwargs['model'].objects.filter(full_name=full_name)
        if fund_person:
            if cost_amount == 0:
                kwargs['form'].add_error('cost_amount', 'لطفا مبلغ هزینه را وارد نمایید')
                fund_valid = False
            if cost_description == '':
                kwargs['form'].add_error('cost_description', 'لطفا شرح هزینه را وارد نمایید')
                fund_valid = False
            if removal_date is None:
                kwargs['form'].add_error('removal_date', 'لطفا تاریخ برداشت را انتخاب نمایید')
                fund_valid = False
            # if kwargs['url_name'] == 'fund_create' and receipt_image is None:
            #     kwargs['form'].add_error('receipt_image', 'لطفا تصویر فیش پرداختی را بارگذاری نمایید')
            #     fund_valid = False
            result_validation = image_size_validation(kwargs['form'], ['receipt_image'])
            if not result_validation:
                fund_valid = False

            sum_costs = fund_person.aggregate(Sum('cost_amount'))['cost_amount__sum']
            sum_charge = fund_person.aggregate(Sum('charge_amount'))['charge_amount__sum']
            total_cash = (sum_charge - sum_costs) - cost_amount
            if total_cash <= 0:
                kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی تنخواه جهت برداشت کافی نمی‌باشد."])
                fund_valid = False
        else:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["تنخواه جدید هیچ موجودی جهت برداشت ندارد."])
            fund_valid = False
    else:
        charge_amount = kwargs['form'].cleaned_data.get('charge_amount')
        charge_date = kwargs['form'].cleaned_data.get('charge_date')
        # charge_image = kwargs['form'].cleaned_data.get('charge_image')
        if charge_amount == 0:
            kwargs['form'].add_error('charge_amount', 'لطفا مبلغ واریزی را وارد نمایید')
            fund_valid = False
        if charge_date is None:
            kwargs['form'].add_error('charge_date', 'لطفا تاریخ واریز را وارد نمایید')
            fund_valid = False
        # if kwargs['url_name'] == 'fund_create' and charge_image is None:
        #     kwargs['form'].add_error('charge_image', 'لطفا تصویر فیش واریزی را بارگذاری نمایید')
        #     fund_valid = False
        result_validation = image_size_validation(kwargs['form'], ['charge_image'])
        if not result_validation:
            fund_valid = False
        
    return fund_valid


def cash_box_validation(**kwargs):
    operation_type = kwargs['form'].cleaned_data.get('operation_type')
    cashbox_valid = True
    if operation_type == 'rem':
        removal_amount = kwargs['form'].cleaned_data.get('removal_amount')
        removal_description = kwargs['form'].cleaned_data.get('removal_description')
        # removal_image = kwargs['form'].cleaned_data.get('removal_image')
        removal_date = kwargs['form'].cleaned_data.get('removal_date')
        rem_operate = kwargs['model'].objects.filter(operation_type='rem')
        set_operate = kwargs['model'].objects.filter(operation_type='set')
        if set_operate:
            if removal_amount == 0:
                kwargs['form'].add_error('removal_amount', 'لطفا مبلغ برداشت را وارد نمایید')
                cashbox_valid = False
            if removal_description == '':
                kwargs['form'].add_error('removal_description', 'لطفا شرح برداشت را وارد نمایید')
                cashbox_valid = False
            if removal_date is None:
                kwargs['form'].add_error('removal_date', 'لطفا تاریخ برداشت را انتخاب نمایید')
                cashbox_valid = False
            # if kwargs['url_name'] == 'cash_box_create' and removal_image is None:
            #     kwargs['form'].add_error('removal_image', 'لطفا تصویر فیش برداشت را بارگذاری نمایید')
            #     cashbox_valid = False
            result_validation = image_size_validation(kwargs['form'], ['removal_image'])
            if not result_validation:
                cashbox_valid = False
            if not rem_operate:
                sum_settles = set_operate.aggregate(Sum('settle_amount'))['settle_amount__sum']
                total_cash = sum_settles - removal_amount
                if total_cash <= 0:
                    kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی صندوق جهت برداشت کافی نمی‌باشد."])
                    cashbox_valid = False
            else:
                sum_removals = rem_operate.aggregate(Sum('removal_amount'))['removal_amount__sum']
                sum_settles = set_operate.aggregate(Sum('settle_amount'))['settle_amount__sum']
                total_cash = (sum_settles - sum_removals) - removal_amount
                if total_cash <= 0:
                    kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی صندوق جهت برداشت کافی نمی‌باشد."])
                    cashbox_valid = False
        else:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["صندوق هیچ موجودی جهت برداشت ندارد."])
            cashbox_valid = False
    else:
        settle_amount = kwargs['form'].cleaned_data.get('settle_amount')
        settle_description = kwargs['form'].cleaned_data.get('settle_description')
        # settle_image = kwargs['form'].cleaned_data.get('settle_image')
        settle_date = kwargs['form'].cleaned_data.get('settle_date')
        if settle_amount == 0:
            kwargs['form'].add_error('settle_amount', 'لطفا مبلغ واریزی را وارد نمایید')
            cashbox_valid = False
        if settle_description == '':
            kwargs['form'].add_error('settle_description', 'لطفا شرح واریز را وارد نمایید')
            cashbox_valid = False
        if settle_date is None:
            kwargs['form'].add_error('settle_date', 'لطفا تاریخ واریز را انتخاب نمایید')
            cashbox_valid = False
        # if kwargs['url_name'] == 'cash_box_create' and settle_image is None:
        #     kwargs['form'].add_error('settle_image', 'لطفا تصویر فیش واریز را بارگذاری نمایید')
        #     cashbox_valid = False
        result_validation = image_size_validation(kwargs['form'], ['settle_image'])
        if not result_validation:
            cashbox_valid = False
    return cashbox_valid


def warehouse_export_validation(**kwargs):
    imp_stuff_amount = kwargs['imp_model'].objects.filter(stuff_type=kwargs['stuff_type']).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    exp_stuff_amount = kwargs['exp_model'].objects.filter(stuff_type=kwargs['stuff_type']).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    total_stuff_amount = 0

    if imp_stuff_amount:
    
        if not exp_stuff_amount:
            total_stuff_amount = imp_stuff_amount
        else:
            total_stuff_amount = imp_stuff_amount - exp_stuff_amount

        if  kwargs['stuff_amount'] > total_stuff_amount:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی کالا در انبار کافی نمی‌باشد."])
            return False
        else:
            return True
        
    else:
        kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["کالا در انبار هیچ موجودی ندارد."])
        return False


def g_date_converter(j_year, j_month, j_day):
    date_tuple = JalaliToGregorian(j_year, j_month, j_day).getGregorianList()
    return f'{date_tuple[0]}-{date_tuple[1]}-{date_tuple[2]}'


def filter_date_values(filter_value):
    now_day = timezone.now().day
    now_month = timezone.now().month
    now_year = timezone.now().year

    now_date_str = f'{now_year}-{now_month}-{now_day}'

    last_week = now_day - 7
    last_month = now_month - 1
    last_year = now_year - 1
    
    if filter_value == "last_week":
        if last_week > 0:
            return [f'{now_year}-{now_month}-{last_week}', now_date_str]
        elif last_month > 0:
            return [f'{now_year}-{last_month}-{last_week + 31}', now_date_str]
        else:
            return [f'{last_year}-{12}-{last_week + 31}', now_date_str]
    elif filter_value == "last_month":
        if last_month > 0:
            return [f'{now_year}-{last_month}-{now_day}', now_date_str]
        else:
            return [f'{last_year}-{12}-{now_day}', now_date_str]
    elif filter_value == "current_year":
        return [g_date_converter(datetime.now().year, 1, 1), now_date_str]
    else:
        return [now_date_str, now_date_str]
    


# def quarter_range_date(year_quarter):
#     now_year = datetime.now().year

#     if year_quarter == "first":
#         return [g_date_converter(now_year, 1, 1), g_date_converter(now_year, 3, 31)]
#     elif year_quarter == "second":
#         return [g_date_converter(now_year, 4, 1), g_date_converter(now_year, 6, 31)]
#     elif year_quarter == "third":
#         return [g_date_converter(now_year, 7, 1), g_date_converter(now_year, 9, 30)]
#     else:
#         return [g_date_converter(now_year, 10, 1), g_date_converter(now_year, 12, 29)]
 

def total_projects_buyers_sellers():
    projects_count = Project.objects.all().count()
    all_projects = Project.objects.order_by('-id').all()
    total_projects_buyers = []
    total_project_buyers = 0
    total_projects_sellers = []
    total_project_sellers = 0
    for i in range(0, projects_count):
        project_buyers = BuyersSellers.objects.filter(project=all_projects[i], buyer_seller='buy').all()
        project_sellers = BuyersSellers.objects.filter(project=all_projects[i], buyer_seller='sel').all()
        if project_buyers:
            total_project_buyers = project_buyers.aggregate(Sum('payment_amount'))['payment_amount__sum']
            total_projects_buyers.append(total_project_buyers)
        else:
            total_projects_buyers.append(0)
        if project_sellers:
            total_project_sellers = project_sellers.aggregate(Sum('payment_amount'))['payment_amount__sum']
            total_projects_sellers.append(total_project_sellers)
        else:
            total_projects_sellers.append(0)
    
    return total_projects_buyers, total_projects_sellers


def total_projects_costs():
    all_projects = Project.objects.order_by('-id').all()
    total_costs_list = []
    total_costs = 0
    for project in all_projects:
        total_costs = total_project_costs(project.title)["total_amount"]
        total_costs_list.append(total_costs)
    
    return total_costs_list


def messages_filters(request):
    all_messages = Message.objects.all()
    sent_messages = all_messages.filter(sender=request.user).order_by('-date_time').all()
    received_messages = all_messages.filter(receiver=request.user).order_by('seen', '-date_time').all()
    archived_messages = [
        received_messages.filter(visible_receiver=True, archive_receiver=True).all(), 
        sent_messages.filter(visible_sender=True, archive_sender=True).all()
    ]
    return {
        'sent_count': sent_messages.filter(visible_sender=True, archive_sender=False).count(), 
        'received_count': received_messages.filter(visible_receiver=True, archive_receiver=False).count(),
        'unseen_count': received_messages.filter(seen=False, visible_receiver=True, archive_receiver=False).count(),
        'received_messages': received_messages.filter(visible_receiver=True, archive_receiver=False).all(),
        'sent_messages': sent_messages.filter(visible_sender=True, archive_sender=False).all(), 
        'archived_received': archived_messages[0],
        'archived_sent': archived_messages[1],
        'archived_count': archived_messages[0].count() + archived_messages[1].count(),
    }


def messages_pagination(request):
    page_number = request.GET.get("page")
    if request.resolver_match.url_name == 'received_messages':
        paginator = Paginator(messages_filters(request)['received_messages'], 10)
        page_obj = paginator.get_page(page_number)
        return page_obj
    elif request.resolver_match.url_name == 'sent_messages':
        paginator = Paginator(messages_filters(request)['sent_messages'], 10)
        page_obj = paginator.get_page(page_number)
        return page_obj
    else:
        archived_messages = Message.objects.filter(
            Q(receiver=request.user, visible_receiver=True, archive_receiver=True) |
            Q(sender=request.user, visible_sender=True, archive_sender=True)
        )
        paginator = Paginator(archived_messages, 10)
        page_obj = paginator.get_page(page_number)
        return page_obj

