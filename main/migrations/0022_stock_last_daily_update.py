# Generated by Django 4.0.6 on 2022-07-29 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_rename_date_stockhistory_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='last_daily_update',
            field=models.DateTimeField(null=True),
        ),
    ]
