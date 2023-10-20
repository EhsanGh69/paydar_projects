from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import Q

from jalali_date import datetime2jalali
from django_jalali.db import models as jmodels



class UserManager(BaseUserManager):
    def search(self, query):
        lookup = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, unique=True, default="بدون شماره", verbose_name="شماره همراه")

    objects = UserManager()

    def jalali_date_joined(self):
        return datetime2jalali(self.date_joined).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
    
    def jalali_last_login(self):
        return datetime2jalali(self.last_login).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
    


class Report(models.Model):
    MODELS = (
        ('receives', 'دریافت‌ها'),
        ('payments', 'پرداخت‌ها'),
        ('activities', 'فعالیت‌ها'),
        ('buyers_sellers', 'خریداران / فروشندگان'),
        ('orders', 'سفارشات'),
        ('work_reference', 'ارجاع کار'),
        ('cheques', 'چک‌ها'),
        ('receive_pay', 'دریافت و پرداخت'),
        ('fund', 'تنخواه'),
        ('warehouse_import', 'کالاهای افزوده شده به انبار'),
        ('bank_receives', 'رسیدهای بانکی'),
    )

    report_type = models.CharField(max_length=30, choices=MODELS, verbose_name='نوع گزارش')
    date_from = jmodels.jDateField(verbose_name='از تاریخ')
    date_to = jmodels.jDateField(verbose_name='تا تاریخ')
    report_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان گزارش')

    class Meta:
        verbose_name = "گزارش"
        verbose_name = "گزارشات"

    def __str__(self):
        return self.report_type





