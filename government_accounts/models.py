from django.db import models
from django.db.models.query import Q
from django.utils import timezone

from django_jalali.db import models as jmodels

from projects.models import Project




class Organization(models.Model):
    organization_name = models.CharField(max_length=50, verbose_name="نام ارگان")

    class Meta:
        verbose_name = "ارگان"
        verbose_name_plural = "ارگان‌ها"


    def __str__(self):
        return self.organization_name
    

class ReceiveManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(organization__organization_name__icontains=query) |
            Q(receive_for__icontains=query) |
            Q(project__title__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()



class Receive(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    receive_for = models.CharField(max_length=250, verbose_name="دریافت بابت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_receives', verbose_name="پروژه")
    receive_amount = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ دریافتی")
    receive_date = jmodels.jDateField(verbose_name="تاریخ دریافت")
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = ReceiveManager()

    class Meta:
        verbose_name = "دریافت"
        verbose_name_plural = "دریافت‌ها"


    def __str__(self):
        return self.receive_for
    
    def formatted_receive_amount(self):
        return "{:,}".format(self.receive_amount)
    

class PaymentManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(organization__organization_name__icontains=query) |
            Q(payment_for__icontains=query) |
            Q(project__title__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Payment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    payment_for = models.CharField(max_length=250, verbose_name="پرداخت بابت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_payments', verbose_name="پروژه")
    payment_amount = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ پرداختی")
    payment_date = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ و ساعت پرداخت")

    objects = PaymentManager()

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"


    def __str__(self):
        return self.payment_for
    
    
    def formatted_payment_amount(self):
        return "{:,}".format(self.payment_amount)
    


class ActivityManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(organization__organization_name__icontains=query) |
            Q(activity_type__icontains=query) |
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Activity(models.Model):
    RESULT_CHOICES = (
        ('fn', 'پایان یافته'),
        ('do', 'در حال انجام'),
        ('ns', 'شروع نشده'),
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="ارگان")
    activity_type = models.CharField(max_length=150, verbose_name="نوع فعالیت")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='government_activities', verbose_name="پروژه")
    activity_date = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ و ساعت فعالیت")
    activity_result = models.CharField(max_length=2, choices=RESULT_CHOICES, verbose_name="نتیجه فعالیت")
    activity_descriptions = models.TextField(verbose_name="توضیحات فعالیت در حال انجام", blank=True)

    objects = ActivityManager()

    class Meta:
        verbose_name = "فعالیت"
        verbose_name_plural = "فعالیت‌ها"


    def __str__(self):
        return self.activity_type

