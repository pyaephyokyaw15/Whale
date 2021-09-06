from django.contrib import admin
from .models import Song, Artist, Mood, Playlist

# Register your models here.
admin.site.register(Song)
admin.site.register(Artist)
admin.site.register(Mood)
admin.site.register(Playlist)
