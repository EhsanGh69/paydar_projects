from django.db import models
from django.db.models.query import Q
from django.utils import timezone

from django_jalali.db import models as jmodels

from projects.models import Project
from government_accounts.models import Organization
from non_government_accounts.models import Contractors, Suppliers, Personnel




class ChequesManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(cheque_for__icontains=query) |
            Q(bank_branch__icontains=query) |
            Q(account_owner__icontains=query) |
            Q(account_party__icontains=query) |
            Q(project__title__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Cheques(models.Model):
    CHEQUE_TYPE_CHOICES = (
        ('exp', 'صدور'),
        ('rec', 'دریافت')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_cheques', verbose_name='پروژه')
    cheque_type = models.CharField(max_length=3, choices=CHEQUE_TYPE_CHOICES, verbose_name='نوع چک')
    cheque_for = models.CharField(max_length=100, verbose_name='بابت')
    cheque_number = models.CharField(max_length=50, verbose_name='شماره چک')
    bank_branch = models.CharField(max_length=50, verbose_name='بانک و شعبه')
    cheque_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ')
    registered = models.BooleanField(default=False, verbose_name='ثبت شده')
    cheque_image = models.ImageField(upload_to='images/cheques', null=True, blank=True, verbose_name='تصویر چک')
    export_receive_date = jmodels.jDateField(verbose_name='تاریخ صدور / دریافت')
    due_date = jmodels.jDateField(verbose_name='تاریخ سررسید')
    account_owner = models.CharField(max_length=250, verbose_name='صاحب حساب')
    account_party = models.CharField(max_length=250, verbose_name='طرف حساب')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = ChequesManager()


    class Meta:
        verbose_name = "چک"
        verbose_name_plural = "چک‌ها"


    def __str__(self):
        return self.cheque_number
    
    def formatted_cheque_amount(self):
        return "{:,}".format(self.cheque_amount)
    

class ReceivePayManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(organization__organization_name__icontains=query) |
            Q(contractor__full_name__icontains=query) |
            Q(supplier__full_name__icontains=query) |
            Q(personnel__full_name__icontains=query) |
            Q(regard_to__icontains=query) |
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class ReceivePay(models.Model):
    RECEIVE_PAY = (
        ('rec', 'دریافت'),
        ('pay', 'پرداخت')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_receive_pays', verbose_name='پروژه')
    organ = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organ_receive_pays', null=True, blank=True, verbose_name='طرف حساب دولتی')
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='contractor_receive_pays', null=True, blank=True, verbose_name='پیمانکار')
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='supplier_receive_pays', null=True, blank=True, verbose_name='تأمین کننده')
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='personnel_receive_pays', null=True, blank=True, verbose_name='پرسنل')
    receive_pay = models.CharField(max_length=3, choices=RECEIVE_PAY, verbose_name='دریافت / پرداخت')
    amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ')
    regard_to = models.CharField(max_length=100, verbose_name='بابت')
    date = jmodels.jDateField(verbose_name='تاریخ')
    receipt_image = models.ImageField(upload_to='images/receive_pays', null=True, blank=True, verbose_name='تصویر فیش')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = ReceivePayManager()
    
    class Meta:
        verbose_name = "دریافت و پرداخت"
        verbose_name_plural = "دریافت‌ها و پرداخت‌ها"


    def __str__(self):
        return self.regard_to
    
    def formatted_amount(self):
        return "{:,}".format(self.amount)
    

class FundManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) |
            Q(cost_description__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Fund(models.Model):
    OPERATION_TYPES = (
        ('rem', 'برداشت'),
        ('set', 'واریز')
    )
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    operation_type = models.CharField(max_length=3, choices=OPERATION_TYPES, verbose_name='نوع عملیات')
    # fund cost
    cost_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, verbose_name='مبلغ هزینه')
    cost_description = models.TextField(null=True, blank=True, verbose_name='شرح هزینه')
    receipt_image = models.ImageField(upload_to='images/fund/receipt_images', null=True, blank=True, verbose_name='تصویر فیش پرداختی')
    removal_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ برداشت')
    # fund charge
    charge_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, verbose_name='مبلغ واریزی')
    charge_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ واریز')
    charge_image = models.ImageField(upload_to='images/fund/charge_images', null=True, blank=True, verbose_name='تصویر فیش واریزی')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = FundManager()

    class Meta:
        verbose_name = "تنخواه"
        verbose_name_plural = "تنخواه"

    def __str__(self):
        return self.full_name
    
    def formatted_cost_amount(self):
        return "{:,}".format(self.cost_amount)
    
    def formatted_charge_amount(self):
        return "{:,}".format(self.charge_amount)
    

class CashBoxManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(settle_description__icontains=query) |
            Q(removal_description__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()
    

class CashBox(models.Model):
    OPERATION_TYPES = (
        ('rem', 'برداشت'),
        ('set', 'واریز'),
    )
    operation_type = models.CharField(max_length=3, choices=OPERATION_TYPES, verbose_name='نوع عملیات')
    # settle:
    settle_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, verbose_name='مبلغ واریزی')
    settle_image = models.ImageField(upload_to='images/cash_box/settle_images', null=True, blank=True, verbose_name='تصویر فیش واریزی')
    settle_description = models.TextField(null=True, blank=True, verbose_name='شرح واریز')
    settle_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ واریز')
    # removal:
    removal_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, verbose_name='مبلغ برداشت')
    removal_image = models.ImageField(upload_to='images/cash_box/removal_images', null=True, blank=True, verbose_name='تصویر فیش برداشت')
    removal_description = models.TextField(null=True, blank=True, verbose_name='شرح برداشت')
    removal_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ برداشت')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = CashBoxManager()


    class Meta:
        verbose_name = "صندوق"
        verbose_name_plural = "صندوق"

    def __str__(self):
        return self.operation_type
    
    def formatted_settle_amount(self):
        return "{:,}".format(self.settle_amount)
    
    def formatted_removal_amount(self):
        return "{:,}".format(self.removal_amount)
