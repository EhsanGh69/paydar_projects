# Generated by Django 4.2.1 on 2023-07-01 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0010_alter_orders_measurement_unit'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NoticeConflictOrders',
            new_name='ConflictOrders',
        ),
    ]
