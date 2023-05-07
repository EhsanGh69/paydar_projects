from django.db import models





class Project(models.Model):
    CONTRACT_CHOICES = (
        ('pc', 'مشارکت در ساخت'),
        ('ow', 'مالکیت'),
        ('pa', 'شراکتی'),
        ('co', 'پیمانی'),
    )
    title = models.CharField(max_length=250, verbose_name="عنوان پروژه")
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, verbose_name="نوع قرارداد")
    owners = models.CharField(max_length=100, verbose_name="مالکین")
    contractual_salary = models.BigIntegerField(default=0, verbose_name="دستمزد قرارداد پیمانی")
    contractual_percentage = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, verbose_name="درصد قرارداد پیمانی")
    costs_estimation = models.BigIntegerField(default=0, editable=False, verbose_name="برآورد ریالی کل هزینه")
  
