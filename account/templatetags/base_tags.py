from django import template
from django.db.models import Sum

from cheques_receive_pay.models import Fund


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
    return {
        "cash": cash,
        "formatted_cash": "{:,}".format(cash)
    }


