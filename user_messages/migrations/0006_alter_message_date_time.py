# Generated by Django 4.2.1 on 2023-12-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0005_remove_message_send_date_message_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
