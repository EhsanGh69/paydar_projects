# Generated by Django 4.2.1 on 2023-06-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('non_government_accounts', '0002_remove_contractors_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personnel',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='suppliers',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='suppliers',
            name='lastname',
        ),
        migrations.AddField(
            model_name='personnel',
            name='full_name',
            field=models.CharField(default='', max_length=250, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AddField(
            model_name='suppliers',
            name='full_name',
            field=models.CharField(default='', max_length=250, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='contractors',
            name='full_name',
            field=models.CharField(max_length=250, verbose_name='نام و نام خانوادگی'),
        ),
    ]
