# Generated by Django 4.0.6 on 2022-08-17 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicWebApplication', '0007_song_song_audio_file_name_song_song_video_file_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='Song_Audio_File_Name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='song',
            name='Song_Cover_File_Name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='song',
            name='Song_Video_File_Name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
