from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import dateformat

User = settings.AUTH_USER_MODEL


# Create your models here.
class Mood(models.Model):
    name = models.CharField(max_length=50)
    # banner = models.ImageField(default='images/mood_banners/default.png', upload_to='images/mood_banners/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_url(self):
        # query string reverse
        # https://stackoverflow.com/questions/4995279/including-a-querystring-in-a-django-core-urlresolvers-reverse-call
        return f"{reverse('songs:songs')}?mood={self.slug}"


class Genre(models.Model):
    name = models.CharField(max_length=50)
    # banner = models.ImageField(default='images/genre_banners/default.png', upload_to='images/genre_banners/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return f"{reverse('songs:songs')}?genre={self.slug}"


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

    def __str__(self):
        return self.title

    # This function(name) creates View on Site button  on detail_song when accessing via admin site.
    def get_absolute_url(self):
        # Automatically creates 'View on Site' button  on detail_song when accessing via admin site.
        return reverse('songs:song_detail', args=[self.id])

    @property
    def favourite_count(self):
        return self.favourite_by.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="comments", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.song}:{self.owner}'

    def serialize(self):  # call from other modules
        created_on = dateformat.DateFormat(self.created_on).format('M. j, Y,  P')
        profile_url = reverse("accounts:profile", kwargs={"username": self.owner.username})

        return {
            "id": self.id,
            "text": self.text,
            "owner": self.owner.username,
            "is_authentic_owner": self.owner.authentic,
            "image": self.owner.profile_picture.url,
            "profile_url": profile_url,
            "song": self.song.title,
            "created_on": created_on,
        }








