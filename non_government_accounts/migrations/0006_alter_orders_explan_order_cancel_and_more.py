# Generated by Django 4.2.1 on 2023-06-30 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0005_buyerssellers_current_roof_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='explan_order_cancel',
            field=models.TextField(blank=True, default='بدون توضیح', null=True, verbose_name='توضیح علت لغو سفارش'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='sending_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ ارسال'),
        ),
    ]