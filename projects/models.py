from django.db import models
from django.db.models.query import Q

from django_jalali.db import models as jmodels



class OwnersManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(full_name__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Owners(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    national_card_image = models.ImageField(upload_to='images/owners/national_cards', null=True, blank=True, verbose_name="تصویر کارت ملی")
    birth_certificate_image = models.ImageField(upload_to='images/owners/birth_certificates', null=True, blank=True, verbose_name="تصویر شناسنامه")
    ownership_document_image = models.ImageField(upload_to='images/owners/ownership_documents', null=True, blank=True, verbose_name="تصویر سند مالکیت")

    objects = OwnersManager()

    class Meta:
        verbose_name = "مالک"
        verbose_name_plural = "مالکین"


    def __str__(self):
        return self.full_name


class ProjectManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(owners__full_name__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


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
    contractual_salary = models.PositiveBigIntegerField(default=0, blank=True, null=True, verbose_name="دستمزد قرارداد پیمانی")
    contractual_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=00.00, verbose_name="درصد قرارداد پیمانی") # type: ignore

    objects = ProjectManager()

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title
    
    def owners_to_str(self):
        return " ،".join([owners.full_name for owners in self.owners.all()])
    owners_to_str.short_description = "مالکین"

    def formatted_contractual_salary(self):
        return "{:,}".format(self.contractual_salary)
    
    def persian_contract_type(self):
        if self.contract_type == 'pc':
            return 'مشارکت در ساخت'
        elif self.contract_type == 'ow':
            return 'مالکیت'
        elif self.contract_type == 'pa':
            return 'شراکتی'
        else:
            return 'پیمانی'


class WorkReferenceManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query) |
            Q(activity_type__icontains=query) |
            Q(referrer__icontains=query) |
            Q(doing_agent__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


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
    result_explan = models.TextField(verbose_name='توضیح نتیجه')
    follow_date = jmodels.jDateField(verbose_name='تاریخ پیگیری')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = WorkReferenceManager()

    class Meta:
        verbose_name = "ارجاع کار"
        verbose_name_plural = "ارجاع کارها"

    def __str__(self):
        return self.activity_type
    

class CostsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()
    

class Costs(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='project_costs',
                                verbose_name='پروژه'
                            )
    # branches costs
    water_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب آب')
    electricity_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب برق')
    gas_branch = models.PositiveIntegerField(default=0, verbose_name='هزینه انشعاب گاز')
    phone_subscription = models.PositiveIntegerField(default=0, verbose_name='هزینه اشتراک تلفن')
    # engineer costs
    designer_office = models.PositiveIntegerField(default=0, verbose_name='هزینه دفتر طراح')
    supervisors = models.PositiveIntegerField(default=0, verbose_name='هزینه ناظرین')
    engineer_system = models.PositiveIntegerField(default=0, verbose_name='هزینه نظام مهندسی')
    sketch_map = models.PositiveIntegerField(default=0, verbose_name='هزینه تهیه نقشه کروکی')
    # mayoralty costs
    export_permit = models.PositiveIntegerField(default=0, verbose_name='هزینه صدور پروانه')
    export_end_work = models.PositiveIntegerField(default=0, verbose_name='هزینه صدور پایان کار')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = CostsManager()


    class Meta:
        verbose_name = "هزینه"
        verbose_name_plural = "هزینه ها"

    def __str__(self):
        return self.project.title
    
    def formatted_water_branch(self):
        return "{:,}".format(self.water_branch)
    
    def formatted_electricity_branch(self):
        return "{:,}".format(self.electricity_branch)
    
    def formatted_gas_branch(self):
        return "{:,}".format(self.gas_branch)
    
    def formatted_phone_subscription(self):
        return "{:,}".format(self.phone_subscription)
    
    def formatted_designer_office(self):
        return "{:,}".format(self.designer_office)
    
    def formatted_supervisors(self):
        return "{:,}".format(self.supervisors)
    
    def formatted_engineer_system(self):
        return "{:,}".format(self.engineer_system)
    
    def formatted_sketch_map(self):
        return "{:,}".format(self.sketch_map)
    
    def formatted_export_permit(self):
        return "{:,}".format(self.export_permit)
    
    def formatted_export_end_work(self):
        return "{:,}".format(self.export_end_work)
    

class PaymentsImagesManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class PaymentsImages(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='project_payment_receipts',
                                verbose_name='پروژه'
                            )
    
    designer_office = models.ImageField(upload_to='images/payment_receipts/designer_office', null=True, blank=True, verbose_name='دفتر طراح')
    supervisors = models.ImageField(upload_to='images/payment_receipts/supervisors', null=True, blank=True, verbose_name='ناظرین')
    engineer_system = models.ImageField(upload_to='images/payment_receipts/engineer_system', null=True, blank=True, verbose_name='نظام مهندسی')
    sketch_map = models.ImageField(upload_to='images/payment_receipts/sketch_map', null=True, blank=True, verbose_name='نقشه کروکی')
    export_permit = models.ImageField(upload_to='images/payment_receipts/export_permit', null=True, blank=True, verbose_name='عوارض صدور پروانه')
    visit_toll = models.ImageField(upload_to='images/payment_receipts/visit_toll', null=True, blank=True, verbose_name='عوارض بازدید')
    education_share = models.ImageField(upload_to='images/payment_receipts/education_share', null=True, blank=True, verbose_name='سهم آموزش و پرورش')
    fire_stations_share = models.ImageField(upload_to='images/payment_receipts/fire_stations_share', null=True, blank=True, verbose_name='سهم آتشنشانی')
    social_security_share = models.ImageField(upload_to='images/payment_receipts/social_security_share', null=True, blank=True, verbose_name='سهم تأمین اجتماعی')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = PaymentsImagesManager()
    

    class Meta:
        verbose_name = "تصویر فیش پرداختی"
        verbose_name_plural = "تصاویر فیش های پرداختی"


    def __str__(self):
        return self.project.title
    