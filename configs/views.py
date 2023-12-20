import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cheques_receive_pay.models import Cheques
from account.models import UserActionsLog
from projects.models import Project
from utils.tools import (
    get_all_logged_in_users, total_projects_buyers_sellers, total_projects_costs, messages_filters
)
from jdatetime import datetime


@login_required
def index(request):
    now_date = datetime.now().date()
    all_cheques = Cheques.objects.all()
    soon_cheques = [cheque for cheque in all_cheques if (cheque.due_date > now_date) and (cheque.due_date.day - now_date.day <= 3)]
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

    context = {
        'soon_cheques': soon_cheques,
        'soon_cheques_count': len(soon_cheques),
        'all_logged_in_users': get_all_logged_in_users().exclude(username=request.user.username),
        'user_logs': user_logs.order_by('-id').all(),
        'projects': json.dumps(projects),
        'total_projects_buyers': json.dumps(total_projects_buyers),
        'total_projects_sellers': json.dumps(total_projects_sellers),
        'total_costs': json.dumps(total_costs),
        'unseen_count': messages_filters(request)['unseen_count']
    }
    
    return render(request, 'home.html', context)
    

def csrf_failure(request, reason=""):
    return render(request, '403.html', {})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request, exception=None):
    return render(request, '500.html', {})


