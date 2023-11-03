from django import template
from django.db.models import Sum

from government_accounts.models import Receive, Payment


register = template.Library()

@register.inclusion_tag("partials/total_amount.html")
def total_project_receives(project_title):
    calc_receives = Receive.objects.filter(project__title=project_title).aggregate(Sum('receive_amount'))['receive_amount__sum']
    total_receives = 0

    if calc_receives:
        total_receives = calc_receives
    
    return {
        "total_amount": total_receives,
        "formatted_total_amount": "{:,}".format(total_receives),
    }


@register.inclusion_tag("partials/total_amount.html")
def total_project_payments(project_title):
    calc_payments = Payment.objects.filter(project__title=project_title).aggregate(Sum('payment_amount'))['payment_amount__sum']
    total_payments = 0

    if calc_payments:
        total_payments = calc_payments
    
    return {
        "total_amount": total_payments,
        "formatted_total_amount": "{:,}".format(total_payments),
    }