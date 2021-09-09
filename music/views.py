from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Artist, Mood
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

class SongListView(ListView):
  model = Song
  template_name = 'music/songs.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'songs' 
  # default contetn name is Post.(or object ). it varies
  # But in html files, we use posts.
  # So, change name.


class ArtistListView(ListView):
  model = Artist
  template_name = 'music/artists.html'
  context_object_name = 'artists' 


def artist_songs(request, artist_id):
    return  render(request, 'music/artist_songs.html', {'artist': Artist.objects.get(pk=artist_id)})

def artist_songs_song(request, artist_id, song_id):
    return  render(request, 'music/artist_songs_song.html', {'artist': Artist.objects.get(pk=artist_id), 'song': Song.objects.get(pk=song_id)})

class MoodListView(ListView):
  model = Mood
  template_name = 'music/moods.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'moods' 



def mood_songs(request, mood_id):
  return  render(request, 'music/mood_songs.html', {'mood': Mood.objects.get(pk=mood_id)})

def mood_songs_song(request, mood_id, song_id):
    return  render(request, 'music/mood_songs_song.html', {'mood': Mood.objects.get(pk=mood_id), 'song': Song.objects.get(pk=song_id)})

def song(request, song_id):
    return render(request, 'music/song.html', {'song': Song.objects.get(id=song_id), 'songs': Song.objects.all()})
  
  
@login_required
def favourite(request):
  return render(request, 'music/favourite_songs.html')


def favourite_songs_song(request, song_id):
  return render(request, 'music/favourite_songs_song.html', {'song': Song.objects.get(pk=song_id)})

def edit(request, song_id):
  song = Song.objects.get(pk=song_id)

  if song in request.user.song_set.all():
    request.user.song_set.remove(song)
  else:
    request.user.song_set.add(song)

  return redirect('favourite')