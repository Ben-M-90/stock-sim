# Generated by Django 4.0.5 on 2022-07-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_stock_business_summary_alter_stock_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='history_data',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='histoy_data_labels',
            field=models.TextField(null=True),
        ),
    ]
