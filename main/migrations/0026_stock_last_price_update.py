# Generated by Django 4.0.6 on 2022-08-09 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_rename__logo_url_stock_logo_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='last_price_update',
            field=models.DateTimeField(null=True),
        ),
    ]
