from django.db import models
from django.utils import timezone
from django.db.models.query import Q

from django_jalali.db import models as jmodels

from projects.models import Project






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
    cheque_type = models.CharField(max_length=3, choices=CHEQUE_TYPE_CHOICES, verbose_name='نوع چک')
    cheque_for = models.CharField(max_length=100, verbose_name='بابت')
    cheque_number = models.CharField(max_length=50, verbose_name='شماره چک')
    bank_branch = models.CharField(max_length=50, verbose_name='بانک و شعبه')
    cheque_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ')
    registered = models.BooleanField(default=False, verbose_name='ثبت شده')
    cheque_image = models.ImageField(upload_to='images/cheques', verbose_name='تصویر چک')
    export_receive_date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ صدور / دریافت')
    due_date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ سررسید')
    account_owner = models.CharField(max_length=250, verbose_name='صاحب حساب')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_cheques', verbose_name='پروژه')
    account_party = models.CharField(max_length=250, verbose_name='طرف حساب')

    objects = ChequesManager()


    class Meta:
        verbose_name = "چک"
        verbose_name_plural = "چک‌ها"


    def __str__(self):
        return self.cheque_number
    
    def formatted_cheque_amount(self):
        return "{:,}".format(self.cheque_amount)
    
    








