# Generated by Django 4.2.1 on 2023-11-11 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('non_government_accounts', '0002_buyerssellers_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerssellers',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_buyers_sellers', to='projects.project', verbose_name='پروژه'),
        ),
    ]
