# Generated by Django 4.2.1 on 2023-07-20 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0011_rename_noticeconflictorders_conflictorders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_suppliers', to='non_government_accounts.suppliers', verbose_name='تأمین کننده'),
        ),
    ]
