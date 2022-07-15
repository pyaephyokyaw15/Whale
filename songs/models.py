from django.db import models
from django.conf import settings
from django.urls import reverse

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
    owner = models.ForeignKey(User, related_name="songs", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    banner = models.ImageField(default='images/song_banners/default.png', upload_to='images/song_banners/')
    audio_file = models.FileField(upload_to='songs/')
    mood = models.ManyToManyField(Mood, blank=True, related_name="songs")
    genre = models.ManyToManyField(Genre, blank=True, related_name="songs")
    favourite_by = models.ManyToManyField(User, related_name="favourite_songs", blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_time']

    @property
    def favourite_count(self):
        return self.favourite_by.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('songs:all_songs')


class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song}:{self.owner}'







