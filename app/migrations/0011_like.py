# Generated by Django 4.1.2 on 2022-12-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_is_liking', models.CharField(max_length=100)),
                ('who_is_being_liked', models.CharField(max_length=100)),
            ],
        ),
    ]
