from django import template
from django.db.models import Sum

from projects_docs.models import ConditionStatements


register = template.Library()

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