from django import template

from projects.models import Costs
from non_government_accounts.templatetags.non_gov_tags import total_project_requests
from projects_docs.templatetags.projects_docs_tags import total_project_salaries

register = template.Library()


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