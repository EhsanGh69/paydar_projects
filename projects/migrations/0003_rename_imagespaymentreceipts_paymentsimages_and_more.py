# Generated by Django 4.2.1 on 2023-07-05 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_workreference_follow_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImagesPaymentReceipts',
            new_name='PaymentsImages',
        ),
        migrations.AlterField(
            model_name='workreference',
            name='result_explan',
            field=models.TextField(verbose_name='توضیح نتیجه'),
        ),
    ]
