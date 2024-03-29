from django.db import models
from django.db.models.query import Q

from django_jalali.db import models as jmodels

from projects.models import Project
from non_government_accounts.models import Suppliers, Personnel, Contractors




class StuffManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(stuff_type__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Stuff(models.Model):
    MEASUREMENT_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('ton', 'تن'),
        ('num', 'عدد'),
        ('bag', 'کیسه'),
    )
    stuff_type = models.CharField(max_length=100, verbose_name='نوع کالا')
    measurement_unit = models.CharField(max_length=3, choices=MEASUREMENT_UNIT_CHOICES, verbose_name='واحد اندازه گیری')
    
    objects = StuffManager()
    

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"

    def __str__(self):
        return f'{self.stuff_type} - واحد: {self.persian_measurement_unit()}'
    
    def persian_measurement_unit(self):
        if self.measurement_unit == "sqm":
            return 'مترمربع' 
        elif self.measurement_unit == "mel":
            return 'متر طول' 
        elif self.measurement_unit == "kgm":
            return 'کیلوگرم' 
        elif self.measurement_unit == "ton":
            return 'تن' 
        elif self.measurement_unit == "num":
            return 'عدد' 
        else:
            return 'کیسه'


class MainWarehouseImportManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(supplier__full_name__icontains=query)|
            Q(receiver__full_name__icontains=query)|
            Q(other_sender__icontains=query)|
            Q(stuff_type__stuff_type__icontains=query)|
            Q(project_returned__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class MainWarehouseImport(models.Model):
    # sender
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='warehouse_import_suppliers', null=True, blank=True,verbose_name='تأمین کننده')
    other_sender = models.TextField(null=True, blank=True, verbose_name='سایر')
    # stuff
    stuff_type = models.ForeignKey(Stuff,on_delete=models.CASCADE,related_name='warehouse_import_stuffs',verbose_name='نوع کالا')
    stuff_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار')
    receiver = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='warehouse_import_personnel', verbose_name='تحویل گیرنده')
    import_date = jmodels.jDateField(verbose_name='تاریخ ورود کالا')
    # returned
    is_returned = models.BooleanField(default=False, verbose_name='کالا مرجوعی است')
    project_returned = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='warehouse_returned_projects', null=True, blank=True,verbose_name='مرجوعی از پروژه')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = MainWarehouseImportManager()


    class Meta:
        verbose_name = "کالای افزوده شده به انبار"
        verbose_name_plural = "کالاهای افزوده شده به انبار"

    def __str__(self):
        return f"{self.stuff_type} - {self.date_time.year}/{self.date_time.month}/{self.date_time.day}" # type: ignore
    
    def formatted_stuff_amount(self):
        return "{:,}".format(self.stuff_amount)
    
    
class MainWarehouseExportManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(personnel__full_name__icontains=query)|
            Q(contractor__full_name__icontains=query)|
            Q(deliverer__full_name__icontains=query)|
            Q(stuff_type__stuff_type__icontains=query)|
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class MainWarehouseExport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='warehouse_export_projects', verbose_name='پروژه')
    # applicant
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='warehouse_export_personnel', null=True, blank=True, verbose_name='پرسنل')
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='warehouse_export_contractors', null=True, blank=True, verbose_name='پیمانکار')
    # stuff
    stuff_type = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name='warehouse_export_stuffs', verbose_name='نوع کالا')
    stuff_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار')
    deliverer = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='warehouse_export_deliverers', verbose_name='تحویل دهنده')
    export_date = jmodels.jDateField(verbose_name='تاریخ خروج کالا')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)

    objects = MainWarehouseExportManager()

    class Meta:
        verbose_name = "کالای خارج شده از انبار"
        verbose_name_plural = "کالاهای خارج شده از انبار"

    def __str__(self):
        return f"{self.stuff_type} - {self.project}"
    
    def formatted_stuff_amount(self):
        return "{:,}".format(self.stuff_amount)
    

class UseCertificateManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(stuff_type__stuff_type__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class UseCertificate(models.Model):
    RETURNED_TO_CHOICES = (
        ('prw', 'انبار پروژه'),
        ('maw', 'انبار اصلی'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='use_certificate_projects',verbose_name='پروژه')
    # stuff
    stuff_type = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name='use_certificate_stuffs', verbose_name='نوع کالا')
    is_deficient = models.BooleanField(default=False, verbose_name='کسری دارد')
    deficient_amount = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='مقدار کسری')
    is_excess = models.BooleanField(default=False, verbose_name='مازاد دارد')
    excess_amount = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='مقدار مازاد')
    start_using_date = jmodels.jDateField(verbose_name='تاریخ شروع مصرف')
    finish_using_date = jmodels.jDateField(verbose_name='تاریخ پایان مصرف')
    # returned
    returned_to = models.CharField(max_length=3, choices=RETURNED_TO_CHOICES, null=True, blank=True, verbose_name='مرجوعی به')
    return_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ ارجاع به انبار')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)
    
    objects = UseCertificateManager()

    class Meta:
        verbose_name = "گواهی مصرف کالا"
        verbose_name_plural = "گواهی‌های مصرف کالا"

    def __str__(self):
        return f"{self.project.title}-{self.stuff_type.stuff_type}: از {self.start_using_date.year}/{self.start_using_date.month}/{self.start_using_date.day} - تا {self.finish_using_date.year}/{self.finish_using_date.month}/{self.finish_using_date.day}"
    
    def formatted_deficient_amount(self):
        return "{:,}".format(self.deficient_amount)
    
    def formatted_excess_amount(self):
        return "{:,}".format(self.excess_amount)


class ProjectWarehouseManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(personnel_apply__full_name__icontains=query)|
            Q(contractor_apply__full_name__icontains=query)|
            Q(personnel_delivery__full_name__icontains=query)|
            Q(contractor_delivery__full_name__icontains=query)|
            Q(stuff_type__stuff_type__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class ProjectWarehouse(models.Model):
    STATUS_CHOICES = (
        ('exp', 'خروج از انبار'),
        ('imp', 'ورود به انبار'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_warehouse_projects',verbose_name='پروژه')
    # applicant
    personnel_apply = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='project_warehouse_personnel_applies',null=True, blank=True,verbose_name='پرسنل')
    contractor_apply = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='project_warehouse_contractors_applies',null=True, blank=True,verbose_name='پیمانکار')
     # stuff
    stuff_type = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name='project_warehouse_stuffs', verbose_name='نوع کالا')
    stuff_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار')
    # deliverer
    personnel_delivery = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='project_warehouse_personnel_deliveries',null=True, blank=True,verbose_name='پرسنل')
    contractor_delivery = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='project_warehouse_contractors_deliveries',null=True, blank=True,verbose_name='پیمانکار')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name='وضعیت')
    export_import_date = jmodels.jDateField(verbose_name='تاریخ ورود/خروج')
    create_record = jmodels.jDateTimeField(auto_now_add=True)
    update_record = jmodels.jDateTimeField(auto_now=True)
    
    objects = ProjectWarehouseManager()


    class Meta:
        verbose_name = "کالای انبار پروژه"
        verbose_name_plural = "کالاهای انبار پروژه"

    def __str__(self):
        if self.status == 'exp':
            return f"{self.stuff_type} - خروج از انبار "
        else:
            return f"{self.stuff_type} - ورود به انبار "
    
    def formatted_stuff_amount(self):
        return "{:,}".format(self.stuff_amount)

