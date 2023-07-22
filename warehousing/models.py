from django.db import models
from django.utils import timezone
from django.db.models.query import Q

from django_jalali.db import models as jmodels


from projects.models import Project
from non_government_accounts.models import Suppliers, Personnel






class Stuff(models.Model):
    MEASUREMENT_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('ton', 'تن'),
        ('num', 'عدد'),
    )
    stuff_type = models.CharField(max_length=100, verbose_name='نوع کالا')
    measurement_unit = models.CharField(max_length=3, 
                                        choices=MEASUREMENT_UNIT_CHOICES, 
                                        verbose_name='واحد اندازه گیری')
    

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"

    def __str__(self):
        return self.stuff_type




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
    MEASUREMENT_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('ton', 'تن'),
        ('num', 'عدد'),
    )
    # sender
    supplier = models.ForeignKey(Suppliers, 
                                on_delete=models.CASCADE, 
                                related_name='warehouse_import_suppliers', 
                                null=True, blank=True,
                                verbose_name='تأمین کننده')
    other_sender = models.TextField(null=True, blank=True, 
                                    verbose_name='سایر')
    
    # stuff
    stuff_type = models.ForeignKey(Stuff,
                                   on_delete=models.CASCADE,
                                   related_name='warehouse_import_stuffs',
                                   verbose_name='نوع کالا')
    measurement_unit = models.CharField(max_length=3, 
                                        choices=MEASUREMENT_UNIT_CHOICES, 
                                        verbose_name='واحد اندازه گیری')
    stuff_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار')

    receiver = models.ForeignKey(Personnel, 
                                on_delete=models.CASCADE, 
                                related_name='warehouse_import_personnel', 
                                verbose_name='تحویل گیرنده')
    date_time = jmodels.jDateTimeField(default=timezone.now,
                                       verbose_name='تاریخ ارسال')
    
    # returned
    is_returned = models.BooleanField(default=False, verbose_name='کالا مرجوعی است')
    project_returned = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='warehouse_returned_projects', 
                                null=True, blank=True,
                                verbose_name='مرجوعی از پروژه')
    
    objects = MainWarehouseImportManager()


    class Meta:
        verbose_name = "کالای افزوده شده به انبار"
        verbose_name_plural = "کالاهای افزوده شده به انبار"

    def __str__(self):
        return f"{self.stuff_type} - {self.date_time.year}/{self.date_time.month}/{self.date_time.day}"
    
    def formatted_stuff_amount(self):
        return "{:,}".format(self.stuff_amount)
    
    



