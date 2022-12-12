# Generated by Django 4.1.2 on 2022-11-29 22:27

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_first_name_profile_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images')),
                ('text_content', models.TextField(max_length=280)),
                ('posted_at', models.DateTimeField(default=datetime.datetime(2022, 11, 29, 19, 27, 48, 51950))),
                ('likes', models.IntegerField(default=0)),
                ('reposts', models.IntegerField(default=0)),
                ('coments', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]