# Generated by Django 4.2.1 on 2023-11-30 05:35

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques_receive_pay', '0003_alter_cashbox_create_record_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashbox',
            name='removal_date',
            field=django_jalali.db.models.jDateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ برداشت'),
        ),
        migrations.AddField(
            model_name='cashbox',
            name='settle_date',
            field=django_jalali.db.models.jDateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ واریز'),
        ),
    ]