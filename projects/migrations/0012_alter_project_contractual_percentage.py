# Generated by Django 4.2.1 on 2023-06-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_project_contractual_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contractual_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='درصد قرارداد پیمانی'),
        ),
    ]
