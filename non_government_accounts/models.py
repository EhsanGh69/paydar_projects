from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from projects.models import Project




class Contractors(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_contractors', verbose_name="پروژه")
    firstname = models.CharField(max_length=150, verbose_name="نام پیمانکار")
    lastname = models.CharField(max_length=200, verbose_name="نام خانوادگی پیمانکار")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی پیمانکار")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس پیمانکار")
    address = models.TextField(verbose_name="آدرس پیمانکار")

    class Meta:
        verbose_name = "پیمانکار"
        verbose_name_plural = "پیمانکاران"


    def __str__(self):
        return f"{self.firstname} {self.lastname}"




class Suppliers(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_suppliers', verbose_name="پروژه")
    firstname = models.CharField(max_length=150, verbose_name="نام تأمین کننده")
    lastname = models.CharField(max_length=200, verbose_name="نام خانوادگی تأمین کننده")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی تأمین کننده")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس تأمین کننده")
    address = models.TextField(verbose_name="آدرس تأمین کننده")

    class Meta:
        verbose_name = "تأمین کننده"
        verbose_name_plural = "تأمین کنندگان"


    def __str__(self):
        return f"{self.firstname} {self.lastname}"




class Personnel(models.Model):
    firstname = models.CharField(max_length=150, verbose_name="نام")
    lastname = models.CharField(max_length=200, verbose_name="نام خانوادگی")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    contract_image = models.ImageField(upload_to='images/personnel', verbose_name="تصویر قرارداد")

    class Meta:
        verbose_name = "پرسنل"
        verbose_name_plural = "پرسنل"


    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def contract_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.contract_image.url))
    contract_tag.short_description = "تصویر قرارداد"


class Partners(models.Model):
    investment_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ سرمایه‌گذاری')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_partners', verbose_name='پروژه')
    contract_image = models.ImageField(upload_to='images/partners', verbose_name="تصویر قرارداد")
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    address = models.TextField(verbose_name="آدرس")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")

    class Meta:
        verbose_name = "شریک"
        verbose_name_plural = "شرکاء"


    def __str__(self):
        return self.full_name
    
    def contract_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.contract_image.url))
    contract_tag.short_description = "تصویر قرارداد"



# class BuyersSellers(models.Model):
#     BUYER_SELLER_CHOICES = (
#         ('buy', 'خریدار'),
#         ('sel', 'فروشنده')
#     )
#     PAYMENT_ORDER_CHOICES = (
#         ('csh', 'نقدی'),
#         ('chq', 'چک'),
#         ('del', 'حین تحویل'),
#         ('dtr', 'انتقال سند'),
#     )
#     buyer_seller = models.CharField(max_length=3, choices=BUYER_SELLER_CHOICES, verbose_name='خریدار / فروشنده')
#     full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
#     phone = models.CharField(max_length=20, verbose_name="شماره تماس")
#     address = models.TextField(verbose_name="آدرس")
#     contract_image = models.ImageField(upload_to='images/buyers_sellers', verbose_name="تصویر قرارداد")
#     payment_order = models.CharField(max_length=3, choices=PAYMENT_ORDER_CHOICES, verbose_name='ترتیب پرداخت')
#     cash_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پرداخت نقدی')
#     cash_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت نقدی')
#     cheque_payment = models.ForeignKey()



