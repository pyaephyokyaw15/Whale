from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Song, Genre, Mood, Comment
from django.urls import reverse
from django.db.models import Q
from .forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json


# Create your views here.
class SongListView(ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'


class SongSearchView(ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            songs = Song.objects.filter(Q(title__icontains=q) | Q(owner__username__icontains=q))
        else:
            songs = Song.objects.all()
        return songs


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
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            temp = comment_form.save(commit=False)
            temp.owner = request.user
            temp.song = song
            temp.save()

        return redirect('songs:song_detail',pk=pk)

    if request.method == "GET":
        next_song = Song.objects.filter(pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.all().first()

        previous_song = Song.objects.filter(pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.all().last()
        comments = Comment.objects.filter(song=song)
        comment_form = CommentForm()

        context = {
            "song": song,
            "next_song": next_song,
            "previous_song": previous_song,
            "comments": comments,
            "comment_form": comment_form
        }
        return render(request, 'songs/song_detail.html', context=context)


@csrf_exempt
@login_required
def song_action(request, pk):
    # Query for requested song
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return JsonResponse({"error": "Song does not exist."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        if data.get("favourite"):
            if request.user in song.favourite_by.all():
                favourite = False
                song.favourite_by.remove(request.user)
            else:
                song.favourite_by.add(request.user)
                favourite = True

        song.save()

        response = {
            "favourite": favourite
        }

        print("Hay It is OK")
        return JsonResponse(response)



