# Generated by Django 4.2.1 on 2023-05-07 16:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
# import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_alter_project_contract_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(choices=[('mu', 'شهرداری'), ('es', 'نظام مهندسی'), ('ss', 'تأمین اجتماعی'), ('wo', 'سازمان پسماند'), ('hd', 'مسکن و شهرسازی'), ('fs', 'آتشنشانی'), ('df', 'دارایی'), ('ec', 'شرکت برق'), ('wc', 'شرکت آبفا'), ('gc', 'شرکت گاز'), ('ot', 'سایر')], max_length=2, verbose_name='ارگان')),
                ('receive_for', models.CharField(max_length=250, verbose_name='دریافت بابت')),
                ('receive_amount', models.BigIntegerField(default=0, verbose_name='مبلغ دریافتی')),
                # ('receive_date', django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ دریافت')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='government_receives', to='projects.project', verbose_name='پروژه')),
            ],
        ),
    ]
