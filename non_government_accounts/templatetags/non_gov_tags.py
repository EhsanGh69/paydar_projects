from django import template
from django.db.models import Sum

from non_government_accounts.models import Orders, Contractors, Suppliers, Partners


register = template.Library()

@register.inclusion_tag("partials/total_amount.html")
def total_project_requests(project_title):
    orders = Orders.objects.filter(project__title=project_title, order_result='snd').all()
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
def total_project_investments(project_title):
    calc_investments = Partners.objects.filter(project__title=project_title).aggregate(Sum('investment_amount'))['investment_amount__sum']
    total_investments = 0

    if calc_investments:
        total_investments = calc_investments
    
    return {
        "total_amount": total_investments,
        "formatted_total_amount": "{:,}".format(total_investments),
    }


@register.inclusion_tag("partials/all_participants.html")
def all_contractors(project_title):
    contractors = Contractors.objects.filter(project__title=project_title).all()
    participants_list = '_'

    if contractors:
        participants_list = " ،".join([contractor.full_name for contractor in contractors])

    return { "participants_list": participants_list }


@register.inclusion_tag("partials/all_participants.html")
def all_suppliers(project_title):
    suppliers = Suppliers.objects.filter(project__title=project_title).all()
    participants_list = '_'

    if suppliers:
        participants_list = " ،".join([supplier.full_name for supplier in suppliers])

    return { "participants_list": participants_list }


@register.inclusion_tag("partials/all_participants.html")
def all_partners(project_title):
    partners = Partners.objects.filter(project__title=project_title).all()
    participants_list = '_'

    if partners:
        participants_list = " ،".join([partner.full_name for partner in partners])

    return { "participants_list": participants_list }
