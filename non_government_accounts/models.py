from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from projects.models import Project
from cheques_receive_pay.models import Cheques



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
    supplier_demand = models.PositiveBigIntegerField(default=0, editable=False)

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



class BuyersSellers(models.Model):
    BUYER_SELLER_CHOICES = (
        ('buy', 'خریدار'),
        ('sel', 'فروشنده')
    )
    PAYMENT_ORDER_CHOICES = (
        ('csh', 'نقدی'),
        ('chq', 'چک'),
        ('del', 'حین تحویل'),
        ('dtr', 'انتقال سند'),
    )
    buyer_seller = models.CharField(max_length=3, choices=BUYER_SELLER_CHOICES, verbose_name='خریدار / فروشنده')
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    contract_image = models.ImageField(upload_to='images/buyers_sellers', verbose_name="تصویر قرارداد")
    payment_order = models.CharField(max_length=3, choices=PAYMENT_ORDER_CHOICES, verbose_name='ترتیب پرداخت')
    cash_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پرداخت نقدی')
    cash_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت نقدی')
    cheque_payment = models.ForeignKey(Cheques,
                                        on_delete=models.CASCADE,
                                        related_name='cheque_payments',
                                        verbose_name='پرداخت به صورت چک',
                                        help_text='شماره چک مورد نظر را انتخاب کنید'
                                    )
    delivery_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت حین تحویل')
    delivery_cheque = models.ForeignKey(Cheques,
                                        on_delete=models.CASCADE,
                                        related_name='cheque_deliveries',
                                        verbose_name='پرداخت حین تحویل به صورت چک',
                                        help_text='شماره چک مورد نظر را انتخاب کنید'
                                    )
    doc_transfer_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت انتقال سند')
    doc_transfer_cheque = models.ForeignKey(Cheques,
                                        on_delete=models.CASCADE,
                                        related_name='cheque_doc_transfers',
                                        verbose_name='پرداخت انتقال سند به صورت چک',
                                        help_text='شماره چک مورد نظر را انتخاب کنید'
                                    )
    

    class Meta:
        verbose_name = "خریدار / فروشنده"
        verbose_name_plural = "خریداران / فروشندگان"


    def __str__(self):
        return self.full_name
    
    def contract_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.contract_image.url))
    contract_tag.short_description = "تصویر قرارداد"



class Orders(models.Model):
    MEASUREMENT_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('num', 'تعداد'),
    )
    ORDER_RESULT_CHOICES = (
        ('spd', 'ارسال در تاریخ مشخص'),
        ('snd', 'ارسال شده'),
        ('cld', 'لغو شده'),
    )
    SENDED_IMAGE_TYPE_CHOICES = (
        ('blg', 'بارنامه'),
        ('fac', 'فاکتور'),
        ('enf', 'برگه ورود'),
        ('exf', 'برگه خروج'),
    )
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='order_supliers', verbose_name='تأمین کننده')
    order_type = models.CharField(max_length=100, verbose_name='نوع سفارش')
    measurement_unit = models.CharField(max_length=3, choices=MEASUREMENT_UNIT_CHOICES, verbose_name='واحد اندازه گیری')
    unit_price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت واحد')
    order_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار سفارش')
    order_total_price = models.PositiveBigIntegerField(default=0, editable=False)
    order_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ و زمان سفارش')
    order_respite = models.PositiveSmallIntegerField(default=0, verbose_name='مهلت سفارش')
    order_result = models.CharField(max_length=3, choices=ORDER_RESULT_CHOICES, verbose_name='نتیجه سفارش')
    sending_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ارسال', help_text='ارسال در تاریخ مشخص')
    sended_image = models.ImageField(upload_to='images/sended_images', verbose_name='تصویر سفارش ارسال شده')
    sended_image_type = models.CharField(max_length=3, choices=SENDED_IMAGE_TYPE_CHOICES, verbose_name='نوع تصویر سفارش ارسال شده')
    explan_order_cancel = models.TextField(default='بدون توضیح')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_orders', verbose_name='پروژه')

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"


    def __str__(self):
        return self.order_type
    
    def sended_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.sended_image.url))
    sended_tag.short_description = "تصویر سفارش ارسال شده"


    def get_order_total_price(self):
        self.order_total_price = self.order_amount * self.unit_price
        return self.order_total_price
    get_order_total_price.short_description = 'قیمت کل سفارش'


    def get_supplier_demand(self):
        self.supplier.supplier_demand += self.order_total_price
        return self.supplier.supplier_demand
    get_supplier_demand.short_description = 'طلب تأمین کننده'


