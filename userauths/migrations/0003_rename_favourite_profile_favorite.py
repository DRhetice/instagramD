# Generated by Django 4.1.2 on 2022-12-08 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_remove_profile_favorite_profile_bio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='favourite',
            new_name='favorite',
        ),
    ]
