# Generated by Django 4.2.1 on 2023-05-20 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0013_remove_suppliers_supplier_demand_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticeconflictorders',
            options={'verbose_name': 'مغایرت سفارش', 'verbose_name_plural': 'مغایرت سفارشات'},
        ),
    ]