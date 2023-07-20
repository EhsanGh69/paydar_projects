# Generated by Django 4.2.1 on 2023-07-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stuff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stuff_type', models.CharField(max_length=100, verbose_name='نوع کالا')),
                ('measurement_unit', models.CharField(choices=[('sqm', 'مترمربع'), ('mel', 'مترطول'), ('kgm', 'کیلوگرم'), ('ton', 'تن'), ('num', 'عدد')], max_length=3, verbose_name='واحد اندازه گیری')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالاها',
            },
        ),
    ]
