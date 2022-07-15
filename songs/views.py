from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Song, Genre, Mood
from django.urls import reverse



# Create your views here.
class SongListView(ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'


class FavouriteSongListView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'




    def get_queryset(self):
        return Song.objects.filter(favourite_by=self.request.user)


class GenreListView(ListView):
    model = Genre
    template_name = 'songs/genres.html'
    context_object_name = 'genres'


class GenreSongListView(ListView):
    model = Genre
    template_name = 'songs/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        genre = Genre.objects.get(slug=self.kwargs.get('slug'))
        return Song.objects.filter(genre=genre)


class MoodListView(ListView):
    model = Mood
    template_name = 'songs/moods.html'
    context_object_name = 'moods'


class MoodSongListView(ListView):
    model = Mood
    template_name = 'songs/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        mood = Mood.objects.get(slug=self.kwargs.get('slug'))
        return Song.objects.filter(mood=mood)




class SongUploadView(CreateView):
    model = Song
    template_name = 'songs/upload.html'
    fields = ['title', 'banner', 'audio_file', 'mood', 'genre']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def song_detail(request, pk):
    song = Song.objects.filter(pk=pk).first()

    next_song = Song.objects.filter(pk__lt=pk).first()
    if not next_song:
        next_song = Song.objects.all().first()

    previous_song = Song.objects.filter(pk__gt=pk).last()
    if not previous_song:
        previous_song = Song.objects.all().last()

    context = {
        "song": song,
        "next_song": next_song,
        "previous_song": previous_song
    }
    return render(request, 'songs/song_detail.html', context=context)