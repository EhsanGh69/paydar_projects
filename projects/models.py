from django.db import models
from django.utils.html import format_html





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
        return " ،".join([owners.full_name for owners in self.owners])
    owners_to_str.short_description = "مالکین"

