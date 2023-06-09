# Generated by Django 4.2.1 on 2023-07-01 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0009_alter_orders_order_date_alter_orders_sending_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='measurement_unit',
            field=models.CharField(choices=[('sqm', 'مترمربع'), ('mel', 'مترطول'), ('kgm', 'کیلوگرم'), ('ton', 'تن'), ('num', 'عدد')], max_length=3, verbose_name='واحد اندازه گیری'),
        ),
    ]
