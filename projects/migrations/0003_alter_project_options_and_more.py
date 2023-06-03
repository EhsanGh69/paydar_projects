# Generated by Django 4.2.1 on 2023-05-07 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_contract_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'پروژه', 'verbose_name_plural': 'پروژه\u200cها'},
        ),
        migrations.AlterField(
            model_name='project',
            name='contractual_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='درصد قرارداد پیمانی'),
        ),
    ]