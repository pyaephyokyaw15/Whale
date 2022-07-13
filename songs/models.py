from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Mood(models.Model):
    name = models.CharField(max_length=50)
    banner = models.ImageField(default='images/mood_banners/default.png', upload_to='images/mood_banners/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    banner = models.ImageField(default='images/genre_banners/default.png', upload_to='images/genre_banners/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=150)
    banner = models.ImageField(default='images/song_banners/default.png', upload_to='images/song_banners/')
    audio_file = models.FileField(upload_to='songs/')
    mood = models.ManyToManyField(Mood, blank=True, related_name="songs")
    genre = models.ManyToManyField(Genre, blank=True, related_name="songs")
    favourite_by = models.ManyToManyField(User, related_name="favourite_songs", blank=True)

    def __str__(self):
        return self.title






