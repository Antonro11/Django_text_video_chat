# Generated by Django 4.2 on 2023-05-24 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='video_on',
            field=models.IntegerField(default=0),
        ),
    ]
