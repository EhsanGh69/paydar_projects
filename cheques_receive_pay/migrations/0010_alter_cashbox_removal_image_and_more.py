# Generated by Django 4.2.1 on 2023-08-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques_receive_pay', '0009_cashbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbox',
            name='removal_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/cash_box/removal_image', verbose_name='تصویر فیش برداشت'),
        ),
        migrations.AlterField(
            model_name='cashbox',
            name='settle_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/cash_box/settle_images', verbose_name='تصویر فیش واریزی'),
        ),
        migrations.AlterField(
            model_name='fund',
            name='charge_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/fund/charge_images', verbose_name='تصویر فیش واریزی'),
        ),
        migrations.AlterField(
            model_name='fund',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/fund/receipt_images', verbose_name='تصویر فیش پرداختی'),
        ),
    ]