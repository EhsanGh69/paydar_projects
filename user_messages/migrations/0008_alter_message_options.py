# Generated by Django 4.2.1 on 2023-12-20 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0007_remove_message_trash_message_archive_receiver_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'پیام', 'verbose_name_plural': 'پیام\u200cها'},
        ),
    ]