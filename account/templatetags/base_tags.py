from django import template
from django.db.models import Sum

from cheques_receive_pay.models import Fund, CashBox


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



@register.inclusion_tag("partials/total_cash.html")
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
        "cash_box": cash_box,
        "formatted_cash_box": "{:,}".format(cash_box)
    }


