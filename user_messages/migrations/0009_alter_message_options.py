# Generated by Django 4.2.1 on 2023-12-20 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0008_alter_message_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'permissions': (('write_message', 'نوشتن پیام'), ('seen_message', 'مشاهده پیام'))},
        ),
    ]
