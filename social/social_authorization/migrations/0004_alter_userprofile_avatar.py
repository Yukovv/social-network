# Generated by Django 4.1 on 2022-08-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_authorization', '0003_alter_userprofile_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/avatars'),
        ),
    ]
