from django.db import models
# from audiofield.fields import AudioField


# Create your models here.
class Mood(models.Model):
    name = models.CharField(max_length=100)
    banner = models.ImageField(default='images/mood_banners/default.png', upload_to='images/mood_banners/')


class Song(models.Model):
    title = models.CharField(max_length=150)
    banner = models.ImageField(default='images/song_banners/default.png', upload_to='images/song_banners/')
    audio_file = models.FileField(upload_to='songs/')
    mood = models.ManyToManyField(Mood)


