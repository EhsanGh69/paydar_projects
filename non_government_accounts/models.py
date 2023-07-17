from django.db import models
from django.utils import timezone
from django.db.models.query import Q

from django_jalali.db import models as jmodels


from projects.models import Project



class ContractorsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) |
            Q(job__icontains=query) |
            Q(project__title__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()

class Contractors(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_contractors', verbose_name="پروژه")
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")

    objects = ContractorsManager()

    class Meta:
        verbose_name = "پیمانکار"
        verbose_name_plural = "پیمانکاران"


    def __str__(self):
        return self.full_name


class SuppliersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) |
            Q(job__icontains=query) |
            Q(project__title__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Suppliers(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_suppliers', verbose_name="پروژه")
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")

    objects = SuppliersManager()

    class Meta:
        verbose_name = "تأمین کننده"
        verbose_name_plural = "تأمین کنندگان"


    def __str__(self):
        return self.full_name



class PersonnelManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) |
            Q(job__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Personnel(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    job = models.CharField(max_length=100, verbose_name="رشته شغلی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    contract_image = models.ImageField(upload_to='images/personnel', verbose_name="تصویر قرارداد")

    objects = PersonnelManager()

    class Meta:
        verbose_name = "پرسنل"
        verbose_name_plural = "پرسنل"


    def __str__(self):
        return self.full_name
    

class PartnersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) |
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()
    

class Partners(models.Model):
    investment_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ سرمایه‌گذاری')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_partners', verbose_name='پروژه')
    contract_image = models.ImageField(upload_to='images/partners', verbose_name="تصویر قرارداد")
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    address = models.TextField(verbose_name="آدرس")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")

    objects = PartnersManager()

    class Meta:
        verbose_name = "شریک"
        verbose_name_plural = "شرکاء"


    def __str__(self):
        return self.full_name
    
    def formatted_investment_amount(self):
        return "{:,}".format(self.investment_amount)



class BuyersSellersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query)|
            Q(address__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


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
        ('afh', 'بعد از سفت‌ کاری'),
        ('aif', 'بعد از اجرای تأسیسات'),
        ('atc', 'بعد از کاشی و سرامیک'),
        ('afc', 'بعد از سقف طبقه'),
        ('aff', 'بعد از فونداسیون'),
        ('oth', 'سایر'),
    )
    
    buyer_seller = models.CharField(max_length=3, choices=BUYER_SELLER_CHOICES, verbose_name='خریدار / فروشنده')
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    contract_image = models.ImageField(upload_to='images/buyers_sellers', verbose_name="تصویر قرارداد")
    payment_order = models.CharField(max_length=3, choices=PAYMENT_ORDER_CHOICES, verbose_name='ترتیب پرداخت')
    current_roof = models.CharField(max_length=50, blank=True, null=True, verbose_name="سقف کنونی")
    payment_date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ پرداخت')
    payment_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداختی')

    objects = BuyersSellersManager()
    

    class Meta:
        verbose_name = "خریدار / فروشنده"
        verbose_name_plural = "خریداران / فروشندگان"


    def __str__(self):
        return self.full_name
    
    def formatted_payment_amount(self):
        return "{:,}".format(self.payment_amount)
    


class OrdersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(supplier__full_name__icontains=query)|
            Q(order_type__icontains=query)|
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Orders(models.Model):
    MEASUREMENT_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('ton', 'تن'),
        ('num', 'عدد'),
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_orders', verbose_name='پروژه')
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='order_supliers', verbose_name='تأمین کننده')
    order_type = models.CharField(max_length=100, verbose_name='نوع سفارش')
    measurement_unit = models.CharField(max_length=3, choices=MEASUREMENT_UNIT_CHOICES, verbose_name='واحد اندازه گیری')
    unit_price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت واحد')
    order_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار سفارش')
    order_total_price = models.PositiveBigIntegerField(default=0, editable=False)
    order_date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ و زمان سفارش')
    order_respite = models.PositiveSmallIntegerField(default=0, verbose_name='مهلت سفارش')
    order_result = models.CharField(max_length=3, choices=ORDER_RESULT_CHOICES, verbose_name='نتیجه سفارش')
    sending_date = jmodels.jDateTimeField(default=timezone.now, null=True, blank=True, verbose_name='تاریخ ارسال')
    sended_image = models.ImageField(upload_to='images/sended_images', null=True, blank=True, verbose_name='تصویر سفارش ارسال شده')
    sended_image_type = models.CharField(max_length=3, choices=SENDED_IMAGE_TYPE_CHOICES, null=True, blank=True, verbose_name='نوع تصویر سفارش ارسال شده')
    explan_order_cancel = models.TextField(null=True, blank=True, verbose_name='توضیح علت لغو سفارش')

    objects = OrdersManager()

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"


    def __str__(self):
        return f"{self.order_type} - {self.supplier} - {self.order_date.year}/{self.order_date.month}/{self.order_date.day}"


    def get_order_total_price(self):
        self.order_total_price = self.order_amount * self.unit_price
        return self.order_total_price
    get_order_total_price.short_description = 'قیمت کل سفارش'

    def formatted_unit_price(self):
        return "{:,}".format(self.unit_price)
    
    def formatted_order_amount(self):
        return "{:,}".format(self.order_amount)
    
    def formatted_order_total_price(self):
        return "{:,}".format(self.get_order_total_price())
    
    def formatted_unit_price(self):
        return "{:,}".format(self.unit_price)
    
    def sended_image_type_label(self):
        label = ''
        if self.sended_image_type == 'blg':
            label = 'بارنامه'
        elif self.sended_image_type == 'fac':
            label = 'فاکتور'
        elif self.sended_image_type == 'enf':
            label = 'برگه ورود'
        else:
            label = 'برگه خروج'
        return label
        


class ConflictOrdersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(order__order_type__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class ConflictOrders(models.Model):
    CONFLICT_TYPE_CHOICES = (
        ('pos', 'بیشتر از سفارش'),
        ('neg', 'کمتر از سفارش'),
    )
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_conflicts', verbose_name='سفارش')
    conflict_type = models.CharField(max_length=3, choices=CONFLICT_TYPE_CHOICES, verbose_name="نوع مغایرت")
    conflict_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار مغایرت')

    objects = ConflictOrdersManager()

    class Meta:
        verbose_name = "مغایرت سفارش"
        verbose_name_plural = "مغایرت سفارشات"


    def __str__(self):
        return f"{self.order.order_type} - {self.conflict_type}"
    
    def formatted_conflict_amount(self):
        return "{:,}".format(self.conflict_amount)

