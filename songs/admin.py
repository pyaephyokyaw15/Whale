from django.contrib import admin
from .models import Song, Mood, Genre, Comment


# Register your models here.
class MoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Song)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment)