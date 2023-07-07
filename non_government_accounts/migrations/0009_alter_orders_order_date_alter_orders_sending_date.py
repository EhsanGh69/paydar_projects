# Generated by Django 4.2.1 on 2023-07-01 08:48

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0008_alter_orders_explan_order_cancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ و زمان سفارش'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='sending_date',
            field=django_jalali.db.models.jDateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ ارسال'),
        ),
    ]
