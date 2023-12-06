import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cheques_receive_pay.models import Cheques
from account.models import UserActionsLog
from projects.models import Project
from utils.tools import get_all_logged_in_users, total_projects_buyers_sellers, total_projects_costs



@login_required # type: ignore
def index(request):
    all_cheques_count = Cheques.objects.all().count()
    exp_cheques_count = Cheques.objects.filter(cheque_type="exp").count()
    rec_cheques_count = Cheques.objects.filter(cheque_type="rec").count()
    user_logs = UserActionsLog.objects.filter(user=request.user).all()
    all_projects = Project.objects.order_by('-id').all()
    if len(all_projects) > 7:
        all_projects = all_projects[:7]
    projects = [project.title for project in all_projects]
    total_projects_buyers = total_projects_buyers_sellers()[0]
    if len(total_projects_buyers) > 7:
        total_projects_buyers = total_projects_buyers[:7]
    total_projects_sellers = total_projects_buyers_sellers()[1]
    if len(total_projects_sellers) > 7:
        total_projects_sellers = total_projects_sellers[:7]
    total_costs = total_projects_costs()
    if len(total_costs) > 7:
        total_costs = total_costs[:7]
    
    if user_logs.count() > 4:
        user_logs[0].delete()
        user_logs[0].save()

    context = {
        'all_cheques_count': all_cheques_count,
        'exp_cheques_count': exp_cheques_count,
        'rec_cheques_count': rec_cheques_count,
        'all_logged_in_users': get_all_logged_in_users(),
        'user_logs': user_logs.order_by('-id').all(),
        'projects': json.dumps(projects),
        'total_projects_buyers': json.dumps(total_projects_buyers),
        'total_projects_sellers': json.dumps(total_projects_sellers),
        'total_costs': json.dumps(total_costs),
    }
    
    return render(request, 'home.html', context)
    

def csrf_failure(request, reason=""):
    return render(request, '403.html', {})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request, exception=None):
    return render(request, '500.html', {})


