# Generated by Django 4.0.6 on 2022-07-29 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_userprofile_user_timezone_stockhistory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockhistory',
            old_name='date',
            new_name='date_time',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='current_price',
        ),
    ]
