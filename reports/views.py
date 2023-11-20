from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone

from jalali_date import datetime2jalali

from government_accounts.models import Receive, Payment, Activity
from non_government_accounts.models import BuyersSellers
from projects.models import Project


class ReceiveReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'government_accounts.view_receive'
    context_object_name = "receive"
    template_name = 'reports/receive_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Receive, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class ActivityReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'government_accounts.view_activity'
    context_object_name = "activity"
    template_name = 'reports/activity_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Activity, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class PaymentReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'government_accounts.view_payment'
    context_object_name = "payment"
    template_name = 'reports/payment_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Payment, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class ProjectReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects.view_project'
    context_object_name = "project"
    template_name = 'reports/project_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class BuyerSellerReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'non_government_accounts.view_buyerssellers'
    context_object_name = "buyer_seller"
    template_name = "reports/buyer_seller_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BuyersSellers, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

