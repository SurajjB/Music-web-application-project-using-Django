# Generated by Django 4.0.6 on 2022-08-06 13:59

import django.core.files.storage
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('MusicWebApplication', '0002_contact_user_alter_song_songaudio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='PhoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongAudio',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='Media/SongAudios'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongCover',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='Media/SongCovers'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongDescription',
            field=models.TextField(blank=True, max_length=425, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongVideo',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='Media/SongVideos'), upload_to=''),
        ),
    ]