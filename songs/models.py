from django.db import models
# from audiofield.fields import AudioField


# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=150)
    banner = models.ImageField(default='song_banners/default.png', upload_to='song_banners/')
    audio_file = models.FileField(upload_to='songs/')