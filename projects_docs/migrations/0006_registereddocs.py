# Generated by Django 4.2.1 on 2023-08-01 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_owners_birth_certificate_image_and_more'),
        ('projects_docs', '0005_conditionstatements'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('owd', 'سند مالکیت'), ('atd', 'سند وکالت'), ('sic', 'گواهی امضاء'), ('unl', 'تعهدنامه')], max_length=3, verbose_name='نوع سند')),
                ('doc_image', models.ImageField(upload_to='images/doc_images', verbose_name='تصویر سند')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_doc_projects', to='projects.project', verbose_name='پروژه\u200c')),
            ],
            options={
                'verbose_name': 'سند ثبتی',
                'verbose_name_plural': 'اسناد ثبتی',
            },
        ),
    ]