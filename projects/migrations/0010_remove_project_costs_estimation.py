# Generated by Django 4.2.1 on 2023-06-12 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_imagespaymentreceipts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='costs_estimation',
        ),
    ]