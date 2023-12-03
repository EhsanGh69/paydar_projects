from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone

from jalali_date import datetime2jalali

from government_accounts.models import Receive, Payment, Activity
from non_government_accounts.models import BuyersSellers, Orders, ConflictOrders
from projects.models import Project, Costs, WorkReference
from projects_docs.models import BankReceipts, ConditionStatements
from cheques_receive_pay.models import Cheques, ReceivePay
from warehousing.models import MainWarehouseImport, MainWarehouseExport, UseCertificate, ProjectWarehouse


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
    

class OrderReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'non_government_accounts.view_orders'
    context_object_name = "order"
    template_name = "reports/order_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Orders, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class CostReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects.view_costs'
    context_object_name = "cost"
    template_name = "reports/cost_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Costs, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context 


class WorkReferenceReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects.view_workreference'
    context_object_name = "work_reference"
    template_name = "reports/work_reference_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(WorkReference, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class ConflictOrdersReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'non_government_accounts.view_conflictorders'
    context_object_name = "conflict_order"
    template_name = "reports/conflict_order_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ConflictOrders, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class BankReceiptReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects_docs.view_bankreceipts'
    context_object_name = "bank_receipt"
    template_name = "reports/bank_receipt_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BankReceipts, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class ConditionStatementReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects_docs.view_conditionstatements'
    context_object_name = "condition_statement"
    template_name = "reports/condition_statement_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ConditionStatements, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class ChequeReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'cheques_receive_pay.view_cheques'
    context_object_name = "cheque"
    template_name = 'reports/cheque_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cheques, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class ReceivePayReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'cheques_receive_pay.view_receivepay'
    context_object_name = "receive_pay"
    template_name = "reports/receive_pay_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ReceivePay, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class MainWarehouseImportReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'warehousing.view_mainwarehouseimport'
    context_object_name = "warehouse_import"
    template_name = "reports/warehouse_import_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(MainWarehouseImport, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class MainWarehouseExportReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'warehousing.view_mainwarehouseexport'
    context_object_name = "warehouse_export"
    template_name = "reports/warehouse_export_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(MainWarehouseExport, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context


class UseCertificateReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'warehousing.view_usecertificate'
    context_object_name = "use_certificate"
    template_name = "reports/use_certificate_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UseCertificate, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
    

class ProjectWarehouseReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'warehousing.view_projectwarehouse'
    context_object_name = "project_warehouse"
    template_name = "reports/project_warehouse_report.html"

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ProjectWarehouse, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_date'] = datetime2jalali(timezone.now()).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
        return context
