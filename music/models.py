from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=250)
    logo = models.FileField()
   
    def __str__(self):
        return self.name

class Mood(models.Model):
    mood = models.CharField(max_length=250)

    def __str__(self):
        return self.mood

class Song(models.Model):
    title = models.CharField(max_length=250)
    audio = models.FileField()
    logo = models.FileField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    favourited = models.ManyToManyField(User)
    
    def __str__(self):
        return self.title + '-' + self.artist.name

class Playlist(models.Model):
    title = models.CharField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    
    def __str__(self):
        return self.title


