# Generated by Django 4.1.2 on 2022-11-29 23:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 29, 23, 54, 15, 445361)),
        ),
    ]