# Generated by Django 4.2.1 on 2023-10-01 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_owners_birth_certificate_image_and_more'),
        ('cheques_receive_pay', '0011_alter_cashbox_removal_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivepay',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='project_receive_pays', to='projects.project', verbose_name='پروژه'), # type: ignore
        ),
    ]
