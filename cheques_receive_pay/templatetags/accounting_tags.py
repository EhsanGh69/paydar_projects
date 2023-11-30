from django import template
from django.db.models import Sum

from cheques_receive_pay.models import Fund, CashBox


register = template.Library()


@register.inclusion_tag("partials/fund_cash.html")
def fund_cash(full_name):
    fund_person = Fund.objects.filter(full_name=full_name)
    sum_costs = fund_person.aggregate(Sum('cost_amount'))
    sum_charge = fund_person.aggregate(Sum('charge_amount'))
    cash = 0
    if not sum_costs:
        cash = sum_charge['charge_amount__sum']
    else:
        cash = sum_charge['charge_amount__sum'] - sum_costs['cost_amount__sum']
    
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