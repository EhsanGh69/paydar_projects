from django.db import models
from django.utils import timezone
from jalali_date import datetime2jalali
from django_jalali.db import models as jmodels

from utils.tools import persian_numbers_converter
from projects.models import Project




class Organization(models.Model):
    organization_name = models.CharField(max_length=50, verbose_name="نام ارگان")
    

    class Meta:
        verbose_name = "ارگان"
        verbose_name_plural = "ارگان‌ها"


    def __str__(self):
        return self.organization_name




class Receive(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    receive_for = models.CharField(max_length=250, verbose_name="دریافت بابت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_receives', verbose_name="پروژه")
    receive_amount = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ دریافتی")
    receive_date = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ و ساعت دریافت")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "دریافت"
        verbose_name_plural = "دریافت‌ها"


    def __str__(self):
        return self.receive_for

    def jalali_receive_date(self):
        jalali_receive = datetime2jalali(self.receive_date).strftime('%d / %m / %Y - %H:%M:%S')
        return persian_numbers_converter(jalali_receive)

    def persian_receive_amount(self):
        formatted_number = "{:,}".format(self.receive_amount)
        receive_amount_str = str(formatted_number)
        return persian_numbers_converter(receive_amount_str)



class Payment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    payment_for = models.CharField(max_length=250, verbose_name="پرداخت بابت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_payments', verbose_name="پروژه")
    payment_amount = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ پرداختی")
    payment_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ و ساعت پرداخت")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"


    def __str__(self):
        return self.payment_for
    



class Activity(models.Model):
    RESULT_CHOICES = (
        ('fn', 'پایان یافته'),
        ('do', 'در حال انجام')
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    activity_type = models.CharField(max_length=150, verbose_name="نوع فعالیت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_activities', verbose_name="پروژه")
    activity_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ و ساعت فعالیت")
    activity_result = models.CharField(max_length=2, choices=RESULT_CHOICES, verbose_name="نتیجه فعالیت")
    activity_descriptions = models.TextField(verbose_name="توضیحات فعالیت در حال انجام", default="بدون توضیح")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "فعالیت"
        verbose_name_plural = "فعالیت‌ها"


    def __str__(self):
        return self.activity_type

