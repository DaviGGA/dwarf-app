# Generated by Django 4.1.2 on 2022-11-29 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_post_image_post_profile_alter_post_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
