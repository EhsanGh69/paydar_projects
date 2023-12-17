# Generated by Django 4.2.1 on 2023-12-03 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActionsLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(choices=[('CR', 'Create Object'), ('UP', 'Update Object'), ('DL', 'Delete Object')], max_length=2)),
                ('log_content', models.CharField(max_length=250)),
                ('log_time', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]