# Generated by Django 4.2.1 on 2023-08-12 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره همراه'),
        ),
    ]
