from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

SongAudioPath = FileSystemStorage(location='Media/SongAudios')
SongCoverPath = FileSystemStorage(location='Media/SongCovers')
SongVideoPath = FileSystemStorage(location='Media/SongVideos')

# Create your models here.

class Profile(models.Model):
    App_User = models.OneToOneField(User, on_delete=models.CASCADE)
    Reset_Password_Token = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.App_User.username
    
class Song(models.Model):
    Serial_Number = models.AutoField(primary_key=True)
    Slug = models.CharField(max_length=50)
    Song_Title = models.CharField(max_length=50)
    Song_Artist = models.CharField(max_length=50)
    Song_Featured_Artist = models.CharField(max_length=50, blank=True, null=True)
    Song_Album = models.CharField(max_length=50, blank=True, null=True)
    Song_Released = models.CharField(max_length=50)
    Song_Lyrics = models.TextField(blank=True, null=True)
    Song_Duration = models.CharField(max_length=6)
    Song_Audio = models.FileField(storage=SongAudioPath)
    Song_Audio_File_Name = models.CharField(max_length=100)
    Song_Cover = models.ImageField(storage=SongCoverPath)
    Song_Cover_File_Name = models.CharField(max_length=100)
    Song_Video = models.FileField(storage=SongVideoPath, blank=True)
    Song_Video_File_Name = models.CharField(max_length=100, blank=True)
    Song_Description = models.TextField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return self.Song_Title + " By " + self.Song_Artist + " - " + self.Song_Duration

class Contact(models.Model):
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email_ID = models.EmailField(max_length=50)
    Phone_Number = PhoneNumberField()
    Description = models.TextField()
    
    def __str__(self):
        return self.First_Name + " " + self.Last_Name + " - " + self.Email_ID