# Generated by Django 4.0.5 on 2022-07-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_userprofile_id_alter_userprofile_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
