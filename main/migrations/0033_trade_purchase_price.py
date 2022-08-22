# Generated by Django 4.0.6 on 2022-08-17 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_rename_portfolio_name_trade_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='purchase_price',
            field=models.DecimalField(decimal_places=8, default=1, max_digits=19),
            preserve_default=False,
        ),
    ]
