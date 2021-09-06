from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Artist, Mood
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.contrib.auth.decorators import login_required


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


class ArtistSongView(ListView):

  template_name = 'music/artist_songs.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'songs'

  def get_queryset(self):
    
    artist = get_object_or_404(Artist, id=self.kwargs.get('artist_id'))
    return Song.objects.filter(artist=artist) 



class MoodListView(ListView):
  model = Mood
  template_name = 'music/moods.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'moods' 




class MoodSongView(ListView):

  template_name = 'music/songs.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'songs'

  def get_queryset(self):
    
    mood = get_object_or_404(Mood, id=self.kwargs.get('mood_id'))
    return Song.objects.filter(mood=mood) 



  
  
@login_required
def favourite(request):
  return render(request, 'music/favourite.html')