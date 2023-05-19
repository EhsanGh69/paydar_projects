from django.db import models
from django.utils.html import format_html
from django.utils import timezone




class Owners(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    national_card_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر کارت ملی")
    birth_certificate_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر شناسنامه")
    ownership_document_image = models.ImageField(upload_to='images/owners', verbose_name="تصویر سند مالکیت")

    class Meta:
        verbose_name = "مالک"
        verbose_name_plural = "مالکین"


    def __str__(self):
        return self.full_name
    
    def national_card_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.national_card_image.url))
    national_card_tag.short_description = "تصویر کارت ملی"

    def birth_certificate_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.birth_certificate_image.url))
    birth_certificate_tag.short_description = "تصویر شناسنامه"

    def ownership_document_tag(self):
        return format_html("<img src='{}' width='100' height='75' style='border-radius: 5px;'>".format(self.ownership_document_image.url))
    ownership_document_tag.short_description = "تصویر سند مالکیت"





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
    costs_estimation = models.PositiveBigIntegerField(default=0, editable=False, verbose_name="برآورد ریالی کل هزینه")


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