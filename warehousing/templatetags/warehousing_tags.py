from django import template
from django.db.models import Sum

from warehousing.models import MainWarehouseImport, MainWarehouseExport, ProjectWarehouse


register = template.Library()


@register.inclusion_tag("partials/total_stock.html")
def total_stock(stuff_type, measurement_unit):
    imp_stuff_amount = MainWarehouseImport.objects.filter(
        stuff_type__stuff_type=stuff_type
    ).aggregate(Sum('stuff_amount'))['stuff_amount__sum']

    exp_stuff_amount = MainWarehouseExport.objects.filter(
        stuff_type__stuff_type=stuff_type
    ).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
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

@register.inclusion_tag("partials/total_stock.html")
def project_total_stock(stuff_type, measurement_unit, project_title):
    imp_stuff_amount = ProjectWarehouse.objects.filter(
        stuff_type__stuff_type=stuff_type, project__title=project_title, status='imp'
    ).aggregate(Sum('stuff_amount'))['stuff_amount__sum']

    exp_stuff_amount = ProjectWarehouse.objects.filter(
        stuff_type__stuff_type=stuff_type, project__title=project_title, status='exp'
    ).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
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
