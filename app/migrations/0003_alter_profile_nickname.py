# Generated by Django 4.1.2 on 2022-10-19 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
