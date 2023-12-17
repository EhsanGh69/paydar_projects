# Generated by Django 4.2.1 on 2023-11-26 11:28

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_workreference_create_record_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='costs',
            name='create_record',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='costs',
            name='update_record',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='paymentsimages',
            name='create_record',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='paymentsimages',
            name='update_record',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now),
        ),
    ]