# Generated by Django 4.2.1 on 2023-07-06 10:57

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques_receive_pay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheques',
            name='due_date',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ سررسید'),
        ),
        migrations.AlterField(
            model_name='cheques',
            name='export_receive_date',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ صدور / دریافت'),
        ),
    ]