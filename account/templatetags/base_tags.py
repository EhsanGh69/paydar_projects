from django import template
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from cheques_receive_pay.models import Fund, CashBox
from warehousing.models import MainWarehouseImport, MainWarehouseExport
from projects_docs.models import ConditionStatements
from non_government_accounts.models import Orders
from projects.models import Costs


register = template.Library()


@register.inclusion_tag("partials/main_menu.html")
def main_menu(request, app_name, list_path_name, create_path_name, update_path_name, search_path_name, icon_type, list_content):
    return {
        "request": request,
        "all_paths": [list_path_name, create_path_name, update_path_name, search_path_name],
        "list_link_name": "{}:{}".format(app_name, list_path_name),
        "icon_type": icon_type,
        "list_content": list_content,
    }


@register.inclusion_tag("partials/fund_cash.html")
def fund_cash(full_name):
    fund_person = Fund.objects.filter(full_name=full_name)
    sum_costs = fund_person.aggregate(Sum('cost_amount'))
    sum_charge = fund_person.aggregate(Sum('charge_amount'))
    cash = sum_charge['charge_amount__sum'] - sum_costs['cost_amount__sum']
    if cash < 0:
        cash = 0
    return {
        "cash": cash,
        "formatted_cash": "{:,}".format(cash)
    }



@register.inclusion_tag("partials/total_amount.html")
def total_cash():
    rem_operate = CashBox.objects.filter(operation_type='rem')
    set_operate = CashBox.objects.filter(operation_type='set')
    
    if set_operate and not rem_operate:
        sum_settles = set_operate.aggregate(Sum('settle_amount'))
        cash_box = sum_settles['settle_amount__sum']
    else:
        sum_removals = rem_operate.aggregate(Sum('removal_amount'))
        sum_settles = set_operate.aggregate(Sum('settle_amount'))
        cash_box = sum_settles['settle_amount__sum'] - sum_removals['removal_amount__sum']
        if cash_box < 0:
            cash_box = 0
    return {
        "total_amount": cash_box,
        "formatted_total_amount": "{:,}".format(cash_box)
    }



@register.inclusion_tag("partials/total_stock.html")
def total_stock(stuff_type, measurement_unit):
    imp_stuff_amount = MainWarehouseImport.objects.filter(stuff_type__stuff_type=stuff_type).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    exp_stuff_amount = MainWarehouseExport.objects.filter(stuff_type__stuff_type=stuff_type).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    total_stuff_amount = 0

    if imp_stuff_amount:
        if not exp_stuff_amount:
            total_stuff_amount = imp_stuff_amount
        else:
            total_stuff_amount = imp_stuff_amount - exp_stuff_amount
    
    return {
        "total_stock": total_stuff_amount,
        "formatted_total_stock": "{:,}".format(total_stuff_amount),
        "measurement_unit": measurement_unit
    }


@register.inclusion_tag("partials/total_amount.html")
def total_project_salaries(project_title):
    calc_salaries = ConditionStatements.objects.filter(project__title=project_title, management_confirm='con').aggregate(Sum('final_deposit_amount'))['final_deposit_amount__sum']
    total_salaries = 0

    if calc_salaries:
        total_salaries = calc_salaries
    
    return {
        "total_amount": total_salaries,
        "formatted_total_amount": "{:,}".format(total_salaries),
    }


@register.inclusion_tag("partials/total_amount.html")
def total_project_requests(project_title):
    orders = Orders.objects.filter(project__title=project_title, order_result='snd')
    total_requests = 0
    order_amounts = []

    if orders:
        for order in orders:
            total_price = order.order_amount * order.unit_price
            order_amounts.append(total_price)
        total_requests = sum(order_amounts)
    
    return {
        "total_amount": total_requests,
        "formatted_total_amount": "{:,}".format(total_requests),
    }


@register.inclusion_tag("partials/total_amount.html")
def total_project_costs(project_title):
    cost_obj = Costs.objects.filter(project__title=project_title).first()
    total_costs = 0
    if cost_obj:
        costs = [cost_obj.water_branch, cost_obj.electricity_branch, cost_obj.gas_branch,cost_obj.phone_subscription,
                cost_obj.designer_office, cost_obj.supervisors, cost_obj.engineer_system, cost_obj.sketch_map,
                cost_obj.export_permit, cost_obj.export_end_work, total_project_requests(project_title)['total_amount'],
                total_project_salaries(project_title)['total_amount']
            ]
        total_costs = sum(costs)
    
    return {
        "total_amount": total_costs,
        "formatted_total_amount": "{:,}".format(total_costs),
    }


@register.filter
def index(iterable, index):
    return iterable[index]


@register.filter
def translate_names(name):
    permission_translate = [_(w).replace('Can', '').replace('add', 'افزودن').replace('change', 'ویرایش').replace('delete', 'حذف').replace('view', 'مشاهده') for w in (name).split()] # type: ignore
    return ' '.join(permission_translate)