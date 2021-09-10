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

def mood_next(request, mood_id, song_id):
  mood = Mood.objects.get(id=mood_id)

  
  next_song = mood.song_set.filter(id__gt=song_id).first()
  if not next_song:
    next_song =  mood.song_set.all().first()
  return redirect('http://127.0.0.1:8000/moods/{}/{}'.format(mood_id, next_song.id))


def mood_prev(request, mood_id, song_id):
  mood = Mood.objects.get(id=mood_id)

  
  prev_song = mood.song_set.filter(id__lt=song_id).last()
  if not prev_song:
    prev_song =  mood.song_set.all().last()
  return redirect('http://127.0.0.1:8000/moods/{}/{}'.format(mood_id, prev_song.id))

def artist_next(request, artist_id, song_id):
  artist= Artist.objects.get(id=artist_id)

  
  next_song = artist.song_set.filter(id__gt=song_id).first()
  if not next_song:
    next_song =  artist.song_set.all().first()
  return redirect('http://127.0.0.1:8000/artists/{}/{}'.format(artist_id, next_song.id))


def artist_prev(request, artist_id, song_id):
  artist = Artist.objects.get(id=artist_id)

  
  prev_song = artist.song_set.filter(id__lt=song_id).last()
  if not prev_song:
    prev_song =  artist.song_set.all().last()
  return redirect('http://127.0.0.1:8000/artists/{}/{}'.format(artist_id, prev_song.id))




def favourite_next(request, song_id):
  

  next_song = request.user.song_set.filter(id__gt=song_id).first()
  if not next_song:
    next_song =  request.user.song_set.all().first()
  return redirect('http://127.0.0.1:8000/favourite/{}'.format(next_song.id))


def favourtie_prev(request,song_id):
  
  prev_song = request.user.song_set.filter(id__lt=song_id).last()
  if not prev_song:
    prev_song =  request.user.song_set.all().last()
  return redirect('http://127.0.0.1:8000/favourite/{}'.format(prev_song.id))




def song_next(request, song_id):
  

  next_song = Song.objects.filter(id__gt=song_id).first()
  if not next_song:
    next_song =  Song.objeccts.all().first()
  return redirect('http://127.0.0.1:8000/songs/{}'.format(next_song.id))


def song_prev(request,song_id):
  
  prev_song = Song.objects.filter(id__lt=song_id).last()
  if not prev_song:
    prev_song =  Song.objects.all().last()
  return redirect('http://127.0.0.1:8000/songs/{}'.format(prev_song.id))


