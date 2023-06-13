from django.db import models
from django.db.models.query import Q
from django.utils import timezone





class OwnersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Owners(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    national_card_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر کارت ملی")
    birth_certificate_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر شناسنامه")
    ownership_document_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر سند مالکیت")

    objects = OwnersManager()

    class Meta:
        verbose_name = "مالک"
        verbose_name_plural = "مالکین"


    def __str__(self):
        return self.full_name



class Project(models.Model):
    CONTRACT_CHOICES = (
        ('pc', 'مشارکت در ساخت'),
        ('ow', 'مالکیت'),
        ('pa', 'شراکتی'),
        ('co', 'پیمانی'),
    )
    title = models.CharField(max_length=250, verbose_name="عنوان پروژه")
    contract_type = models.CharField(max_length=2, choices=CONTRACT_CHOICES, verbose_name="نوع قرارداد")
    owners = models.ManyToManyField(Owners, related_name="projects", verbose_name="مالکین")
    contractual_salary = models.PositiveBigIntegerField(default=0, verbose_name="دستمزد قرارداد پیمانی")
    contractual_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="درصد قرارداد پیمانی")


    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title
    
    def owners_to_str(self):
        return " ،".join([owners.full_name for owners in self.owners.all()])
    owners_to_str.short_description = "مالکین"



class WorkReference(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='project_work_references',
                                verbose_name='پروژه'
                            )
    activity_type = models.CharField(max_length=250, verbose_name='نوع فعالیت')
    referrer = models.CharField(max_length=250, verbose_name='ارجاع دهنده')
    doing_agent = models.CharField(max_length=250, verbose_name='مأمور انجام')
    follow_confirm = models.BooleanField(default=False, verbose_name='تأیید پیگیری')
    follow_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پیگیری')
    result_explan = models.TextField(default='بدون توضیح')

    class Meta:
        verbose_name = "ارجاع کار"
        verbose_name_plural = "ارجاع کارها"

    def __str__(self):
        return self.activity_type
    


class Costs(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='project_costs',
                                verbose_name='پروژه'
                            )
    water_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب آب')
    electricity_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب برق')
    gas_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب گاز')
    phone_subscription = models.PositiveIntegerField(default=0, verbose_name='هزینه اشتراک تلفن')
    designer_office = models.PositiveIntegerField(default=0, verbose_name='هزینه دفتر طراح')
    supervisors = models.PositiveIntegerField(default=0, verbose_name='هزینه ناظرین')
    engineer_system = models.PositiveIntegerField(default=0, verbose_name='هزینه نظام مهندسی')
    sketch_map = models.PositiveIntegerField(default=0, verbose_name='هزینه نقشه کروکی')
    export_permit = models.PositiveIntegerField(default=0, verbose_name='هزینه صدور پروانه')
    export_end_work = models.PositiveIntegerField(default=0, verbose_name='هزینه صدور پایان کار')


    class Meta:
        verbose_name = "هزینه"
        verbose_name_plural = "هزینه ها"

    def __str__(self):
        return self.project.title
    


class ImagesPaymentReceipts(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='project_payment_receipts',
                                verbose_name='پروژه'
                            )
    
    designer_office = models.ImageField(upload_to='images/payment_receipts', verbose_name='دفتر طراح')
    supervisors = models.ImageField(upload_to='images/payment_receipts', verbose_name='ناظرین')
    engineer_system = models.ImageField(upload_to='images/payment_receipts', verbose_name='نظام مهندسی')
    sketch_map = models.ImageField(upload_to='images/payment_receipts', verbose_name='نقشه کروکی')
    export_permit = models.ImageField(upload_to='images/payment_receipts', verbose_name='عوارض صدور پروانه')
    visit_toll = models.ImageField(upload_to='images/payment_receipts', verbose_name='عوارض بازدید')
    education_share = models.ImageField(upload_to='images/payment_receipts', verbose_name='سهم آموزش و پرورش')
    fire_stations_share = models.ImageField(upload_to='images/payment_receipts', verbose_name='سهم آتشنشانی')
    social_security_share = models.ImageField(upload_to='images/payment_receipts', verbose_name='سهم تأمین اجتماعی')
    

    class Meta:
        verbose_name = "تصویر فیش پرداختی"
        verbose_name_plural = "تصاویر فیش های پرداختی"


    def __str__(self):
        return self.project.title
    
