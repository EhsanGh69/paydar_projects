from django.db import models
from django.db.models.query import Q

from django_jalali.db import models as jmodels


from projects.models import Project
from non_government_accounts.models import Contractors




class ContractsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(related_to_project__title__icontains=query)|
            Q(unrelated_to_project__icontains=query)|
            Q(contract_title__icontains=query)|
            Q(contract_party__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Contracts(models.Model):
    CONTRACT_TYPE_CHOICES = (
        ('buy', 'خرید'),
        ('sal', 'فروش'),
        ('exc', 'معاوضه')
    )
    related_to_project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='contract_projects',
                                null=True, blank=True,
                                verbose_name='مرتبط با پروژه‌ها')
    unrelated_to_project = models.TextField(null=True, blank=True, verbose_name='غیرمرتبط با پروژه‌ها')

    contract_type = models.CharField(max_length=3, choices=CONTRACT_TYPE_CHOICES, verbose_name='نوع قرارداد')
    contract_title = models.CharField(max_length=250, verbose_name='عنوان قرارداد')
    contract_party = models.CharField(max_length=250, verbose_name='طرف قرارداد')
    contract_image = models.ImageField(upload_to='images/contract_images', verbose_name='تصویر قرارداد')
    contract_date = jmodels.jDateField(verbose_name='تاریخ قرارداد')

    objects = ContractsManager()

    class Meta:
        verbose_name = "قرارداد"
        verbose_name_plural = "قراردادها"

    def __str__(self):
        return self.contract_title
    
    


class ProceedingsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(account_party__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Proceedings(models.Model):
    PROCEEDING_TYPE_CHOICES = (
        ('del', 'تحویل'),
        ('oth', 'متفرقه')
    )
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='proceeding_projects',
                                verbose_name='پروژه‌')
    account_party = models.CharField(max_length=250, verbose_name='طرف حساب')
    proceeding_type = models.CharField(max_length=3, choices=PROCEEDING_TYPE_CHOICES, verbose_name='نوع صورت جلسه')
    proceeding_image = models.ImageField(upload_to='images/proceeding_image', verbose_name='تصویر صورت جلسه')
    proceeding_date = jmodels.jDateField(verbose_name='تاریخ صورت جلسه')

    objects = ProceedingsManager()

    class Meta:
        verbose_name = 'صورت جلسه'
        verbose_name_plural = 'صورت جلسه‌ها'

    def __str__(self):
        return f'{self.account_party} - پروژه {self.project}'
    



class AgreementsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(account_party__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Agreements(models.Model):
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='agreement_projects',
                                verbose_name='پروژه‌')
    account_party = models.CharField(max_length=250, verbose_name='طرف حساب')
    agreement_image = models.ImageField(upload_to='images/agreement_images', verbose_name='تصویر توافق‌نامه')
    agreement_date = jmodels.jDateField(verbose_name='تاریخ توافق‌نامه')
    
    objects = AgreementsManager()

    class Meta:
        verbose_name = 'توافق‌نامه'
        verbose_name_plural = 'توافق‌نامه‌ها'

    def __str__(self):
        return f'{self.account_party} - پروژه {self.project}'



class BankReceiptsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()

class BankReceipts(models.Model):
    RECEIVE_PAY_CHOICES = (
        ('rec', 'دریافت'),
        ('pay', 'پرداخت')
    )
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='bank_receipt_projects',
                                verbose_name='پروژه‌')
    receive_or_pay = models.CharField(max_length=3, choices='', verbose_name='دریافت / پرداخت')
    receipt_date = jmodels.jDateField(verbose_name='تاریخ')
    receipt_image = models.ImageField(upload_to='images/receipt_images', verbose_name='تصویر رسید بانکی')

    objects = BankReceiptsManager()

    class Meta:
        verbose_name = 'رسید بانکی'
        verbose_name_plural = 'رسیدهای بانکی'

    def __str__(self):
        if self.receive_or_pay == 'rec':
            return f'رسید دریافت - پروژه {self.project}'
        else:
            return f'رسید پرداخت - پروژه {self.project}'
        


class ConditionStatementsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(contractor__full_name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class ConditionStatements(models.Model):
    WORK_UNIT_CHOICES = (
        ('sqm', 'مترمربع'),
        ('mel', 'مترطول'),
        ('kgm', 'کیلوگرم'),
        ('ton', 'تن'),
    )
    CONFIRM_CHOICES = (
        ('con', 'تأیید شده'),
        ('nco', 'تأیید نشده'),
        ('awc', 'در انتظار تأیید')
    )
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='condition_statement_projects',
                                verbose_name='پروژه‌')
    contractor = models.ForeignKey(Contractors, 
                                on_delete=models.CASCADE, 
                                related_name='condition_statement_contractors',
                                verbose_name='پیمانکار')
    work_unit = models.CharField(max_length=3, choices=WORK_UNIT_CHOICES, verbose_name='واحد کار')
    requested_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True,
                                                       verbose_name='مبلغ درخواستی')
    confirmed_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, 
                                                      verbose_name='مبلغ تایید شده')
    accounting_confirm = models.CharField(max_length=3, default='awc', choices=CONFIRM_CHOICES,
                                           verbose_name='وضعیت تأیید حسابداری')
    management_confirm = models.CharField(max_length=3, default='awc', choices=CONFIRM_CHOICES,
                                           verbose_name='وضعیت تأیید مدیریت')
    final_deposit_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True, 
                                                      verbose_name='مبلغ واریزی نهایی')
    
    objects = ConditionStatementsManager()

    class Meta:
        verbose_name = 'صورت وضعیت'
        verbose_name_plural = 'صورت وضعیت‌ها'

    def __str__(self):
        return f'صورت وضعیت {self.contractor} - پروژه {self.project}'




class RegisteredDocsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()
    

class RegisteredDocs(models.Model):
    DOC_TYPE_CHOICES = (
        ('owd', 'سند مالکیت'),
        ('atd', 'سند وکالت'),
        ('sic', 'گواهی امضاء'),
        ('unl', 'تعهدنامه'),
    )
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='registered_doc_projects',
                                verbose_name='پروژه‌')
    doc_type = models.CharField(max_length=3, choices=DOC_TYPE_CHOICES, verbose_name='نوع سند')
    doc_image = models.ImageField(upload_to='images/registered_doc_images', verbose_name='تصویر سند')

    objects = RegisteredDocsManager()

    class Meta:
        verbose_name = 'سند ثبتی' 
        verbose_name_plural = 'اسناد ثبتی'

    def __str__(self):
        return f'سند {self.doc_type} - پروژه {self.project}'
    



class OfficialDocsManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(project__title__icontains=query)|
            Q(doc_title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class OfficialDocs(models.Model):
    DOC_TYPE_CHOICES = (
        ('let', 'نامه'),
        ('lic', 'پروانه'),
        ('crt', 'گواهی')
    )
    LETTER_TYPE_CHOICES = (
        ('snd', 'ارسالی'),
        ('rec', 'دریافتی')
    )
    LICENSE_TYPE_CHOICES = (
        ('des', 'تخریب'),
        ('con', 'ساخت'),
        ('dac', 'تخریب و ساخت'),
        ('tci', 'شناسنامه فنی')
    )
    project = models.ForeignKey(Project, 
                                on_delete=models.CASCADE, 
                                related_name='official_docs_projects',
                                verbose_name='پروژه‌')
    
    doc_type = models.CharField(max_length=3, choices=DOC_TYPE_CHOICES, verbose_name='نوع سند')
    letter_type = models.CharField(max_length=3, choices=LETTER_TYPE_CHOICES,
                                   null=True, blank=True,
                                    verbose_name='نوع سند')
    license_type = models.CharField(max_length=3, choices=LETTER_TYPE_CHOICES,
                                    null=True, blank=True,
                                    verbose_name='نوع سند')
    doc_title = models.CharField(max_length=250, verbose_name='عنوان سند')
    doc_image = models.ImageField(upload_to='images/official_doc_images', verbose_name='تصویر سند')
    send_receive_date = jmodels.jDateField(verbose_name='تاریخ ارسال / دریافت')

    objects = OfficialDocsManager()

    class Meta:
        verbose_name = 'سند اداری'
        verbose_name_plural = 'اسناد اداری'

    def __str__(self):
        return f'{self.doc_type} - {self.doc_title} - {self.project}'



