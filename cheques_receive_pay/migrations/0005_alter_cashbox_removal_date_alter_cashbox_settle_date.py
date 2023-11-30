# Generated by Django 4.2.1 on 2023-11-30 05:38

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques_receive_pay', '0004_cashbox_removal_date_cashbox_settle_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbox',
            name='removal_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ برداشت'),
        ),
        migrations.AlterField(
            model_name='cashbox',
            name='settle_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ واریز'),
        ),
    ]
