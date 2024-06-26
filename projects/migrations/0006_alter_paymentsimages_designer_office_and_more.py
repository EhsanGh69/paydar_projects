# Generated by Django 4.2.1 on 2024-04-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_costs_create_record_alter_costs_update_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentsimages',
            name='designer_office',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/designer_office', verbose_name='دفتر طراح'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='education_share',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/education_share', verbose_name='سهم آموزش و پرورش'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='engineer_system',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/engineer_system', verbose_name='نظام مهندسی'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='export_permit',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/export_permit', verbose_name='عوارض صدور پروانه'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='fire_stations_share',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/fire_stations_share', verbose_name='سهم آتشنشانی'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='sketch_map',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/sketch_map', verbose_name='نقشه کروکی'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='social_security_share',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/social_security_share', verbose_name='سهم تأمین اجتماعی'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='supervisors',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/supervisors', verbose_name='ناظرین'),
        ),
        migrations.AlterField(
            model_name='paymentsimages',
            name='visit_toll',
            field=models.ImageField(blank=True, null=True, upload_to='images/payment_receipts/visit_toll', verbose_name='عوارض بازدید'),
        ),
    ]
