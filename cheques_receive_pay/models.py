from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from projects.models import Project






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
    export_receive_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ صدور / دریافت')
    due_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ سررسید')
    account_owner = models.CharField(max_length=250, verbose_name='صاحب حساب')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_cheques', verbose_name='پروژه')
    account_party = models.CharField(max_length=250, verbose_name='طرف حساب')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    class Meta:
        verbose_name = "چک"
        verbose_name_plural = "چک‌ها"


    def __str__(self):
        return self.cheque_number
    
    def cheque_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.cheque_image.url))
    cheque_tag.short_description = "تصویر چک"








