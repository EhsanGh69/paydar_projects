# Generated by Django 4.2.1 on 2024-11-17 17:45

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=50, verbose_name='نام ارگان')),
            ],
            options={
                'verbose_name': 'ارگان',
                'verbose_name_plural': 'ارگان\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Receive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_for', models.CharField(max_length=250, verbose_name='دریافت بابت')),
                ('receive_amount', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ دریافتی')),
                ('receive_date', django_jalali.db.models.jDateField(verbose_name='تاریخ دریافت')),
                ('create_record', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('update_record', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='government_accounts.organization', verbose_name='ارگان')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='government_receives', to='projects.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'دریافت',
                'verbose_name_plural': 'دریافت\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_for', models.CharField(max_length=250, verbose_name='پرداخت بابت')),
                ('payment_amount', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداختی')),
                ('payment_date', django_jalali.db.models.jDateField(verbose_name='تاریخ پرداخت')),
                ('create_record', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('update_record', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='government_accounts.organization', verbose_name='ارگان')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='government_payments', to='projects.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=150, verbose_name='نوع فعالیت')),
                ('activity_result', models.CharField(choices=[('fn', 'پایان یافته'), ('do', 'در حال انجام'), ('ns', 'شروع نشده')], max_length=2, verbose_name='نتیجه فعالیت')),
                ('activity_descriptions', models.TextField(blank=True, verbose_name='توضیحات فعالیت در حال انجام')),
                ('activity_date', django_jalali.db.models.jDateField(verbose_name='تاریخ فعالیت')),
                ('create_record', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('update_record', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='government_accounts.organization', verbose_name='ارگان')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='government_activities', to='projects.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'فعالیت',
                'verbose_name_plural': 'فعالیت\u200cها',
            },
        ),
    ]
