# Generated by Django 4.2.1 on 2023-12-06 10:42

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='send_date',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]
