# Generated by Django 4.1 on 2022-08-18 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_authorization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='images/avatars'),
        ),
    ]
