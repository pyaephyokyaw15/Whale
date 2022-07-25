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
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
class SongListView(ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        mood_query = self.request.GET.get('mood')
        genre_query = self.request.GET.get('genre')
        favourite_query = self.request.GET.get('favourite')
        following_query = self.request.GET.get('following')
        q = self.request.GET.get('q')

        if mood_query:
            self.query_string = f"mood={mood_query}"
            return Song.objects.filter(mood__slug=mood_query)


        elif genre_query:
            self.query_string = f"genre={genre_query}"
            return Song.objects.filter(genre__slug=genre_query)

        elif favourite_query:
            self.query_string = f"favourite=True"
            if self.request.user.is_authenticated:
                return Song.objects.filter(favourite_by=self.request.user)
            else:
                return None

        elif following_query:
            self.query_string = f"following=True"
            if self.request.user.is_authenticated:
                return Song.objects.filter(owner__in=self.request.user.following.all())
            else:
                return None

        elif q:
            self.query_string = ''
            return Song.objects.filter(Q(title__icontains=q) | Q(owner__username__icontains=q))

        else:
            self.query_string = ''
            return Song.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)
        context['query_string'] = self.query_string
        return context






class FavouriteSongListView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'


    def get_queryset(self):
        return Song.objects.filter(favourite_by=self.request.user)





class SongUploadView(LoginRequiredMixin,CreateView):
    model = Song
    template_name = 'songs/upload.html'
    fields = ['title', 'banner', 'audio_file', 'mood', 'genre']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def song_detail(request, pk):
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return HttpResponseNotFound("User does not exist")

    mood_query = request.GET.get('mood')
    genre_query = request.GET.get('genre')
    favourite_query = request.GET.get('favourite')
    following_query = request.GET.get('following')

    if mood_query:
        next_song = Song.objects.filter(mood__slug=mood_query, pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.filter(mood__slug=mood_query).first()

        previous_song = Song.objects.filter(mood__slug=mood_query, pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.filter(mood__slug=mood_query).last()

        query_string = f"mood={mood_query}"

    elif genre_query:
        next_song = Song.objects.filter(genre__slug=genre_query, pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.filter(genre__slug=genre_query).first()

        previous_song = Song.objects.filter(genre__slug=genre_query, pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.filter(genre__slug=genre_query).last()

        query_string = f"genre={genre_query}"

    elif favourite_query:
        next_song = Song.objects.filter(favourite_by=request.user, pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.filter(favourite_by=request.user).first()

        previous_song = Song.objects.filter(favourite_by=request.user, pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.filter(favourite_by=request.user).last()

        query_string = f"favourite=True"

    elif following_query:
        print("THis is following query")
        next_song = Song.objects.filter(owner__in=request.user.following.all(), pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.filter(owner__in=request.user.following.all()).first()

        previous_song = Song.objects.filter(owner__in=request.user.following.all(), pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.filter(owner__in=request.user.following.all()).last()

        query_string = f"following=True"

    else:
        next_song = Song.objects.filter(pk__lt=pk).first()
        if not next_song:
            next_song = Song.objects.all().first()

        previous_song = Song.objects.filter(pk__gt=pk).last()
        if not previous_song:
            previous_song = Song.objects.all().last()

        query_string = ''

    comments = Comment.objects.filter(song=song)
    comment_form = CommentForm()

    context = {
        "song": song,
        "next_song": next_song,
        "previous_song": previous_song,
        "comments": comments,
        "comment_form": comment_form,
        "query_string": query_string
    }
    return render(request, 'songs/song_detail.html', context=context)


@csrf_exempt
def song_detail_action(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'false', 'message': 'User is not authenticated'}, status=403)

    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return HttpResponseNotFound("User does not exist")

    if request.method == "POST":
        data = json.loads(request.body)
        comment_form = CommentForm(data)
        if comment_form.is_valid():
            temp = comment_form.save(commit=False)
            temp.owner = request.user
            temp.song = song
            temp.save()

        return JsonResponse(temp.serialize())

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












