# Generated by Django 4.2.1 on 2023-07-28 11:36

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('warehousing', '0005_projectwarehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usecertificate',
            name='finish_using_date',
            field=django_jalali.db.models.jDateField(verbose_name='تاریخ پایان مصرف'),
        ),
        migrations.AlterField(
            model_name='usecertificate',
            name='return_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ ارجاع به انبار'),
        ),
        migrations.AlterField(
            model_name='usecertificate',
            name='start_using_date',
            field=django_jalali.db.models.jDateField(verbose_name='تاریخ شروع مصرف'),
        ),
    ]
