# Generated by Django 4.2.1 on 2023-05-19 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0011_suppliers_supplier_demand_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='explan_order_cancel',
            field=models.TextField(default='بدون توضیح', verbose_name='توضیح علت لغو سفارش'),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='supplier_demand',
            field=models.PositiveBigIntegerField(editable=False),
        ),
    ]
