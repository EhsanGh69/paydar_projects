# Generated by Django 4.2.1 on 2023-06-09 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government_accounts', '0005_alter_activity_activity_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_descriptions',
            field=models.TextField(blank=True, verbose_name='توضیحات فعالیت در حال انجام'),
        ),
    ]