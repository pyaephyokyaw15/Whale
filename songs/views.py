from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Song, Comment
from django.urls import reverse
from django.db.models import Q
from .forms import CommentForm, SongUploadForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import HttpResponseNotFound

domain = 'http://127.0.0.1:8000/'  # change your domain


# Create your views here.
class SongListView(ListView):
    model = Song
    template_name = 'songs/songs.html'
    context_object_name = 'songs'
    query_string = ''  # sustain the current query_string for further use.
    # e.g. determining the next and previous songs according to the search_query.

    def get_queryset(self):
        mood_query = self.request.GET.get('mood')
        genre_query = self.request.GET.get('genre')
        favourite_query = self.request.GET.get('favourite')
        following_query = self.request.GET.get('following')
        q = self.request.GET.get('q')

        # query-string filter
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

        # search song(search through title and song-owner)
        elif q:
            self.query_string = ''
            return Song.objects.filter(Q(title__icontains=q) | Q(owner__username__icontains=q))

        else:
            self.query_string = ''
            return Song.objects.all()

    # add more elements into the existing context_data when it is sent to the template
    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)
        context['query_string'] = self.query_string
        return context


class SongUploadView(LoginRequiredMixin, CreateView):
    model = Song
    template_name = 'songs/upload.html'
    form_class = SongUploadForm

    def form_valid(self, form):
        # assign the song_owner to current user
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SongEditView(LoginRequiredMixin, UpdateView):
    model = Song
    template_name = 'songs/edit-song.html'
    form_class = SongUploadForm

    def form_valid(self, form):
        # assign the song_owner to current user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        view_name = 'songs:song_detail'
        return reverse(view_name, kwargs={'pk': self.object.pk})


class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song

    def get_success_url(self):
        # retrieve data from the session_store
        current_song_id = self.request.session['current_song_id']
        next_song_id = self.request.session['next_song_id']
        query_string = self.request.session['query_string']

        # If current_song and next_song are equal, it means there is only one song left.
        # In this situation, if we delete the current song, the next song does not exist.
        # So, we need to check this .
        next_song_exist = current_song_id != next_song_id

        # if next_song exists, go to next_song
        # else, go to the song_list according to query_string
        if next_song_exist:
            return domain + 'songs/{}/?{}'.format(next_song_id, query_string)
        else:
            return domain + 'songs/?{}'.format(query_string)


def song_detail(request, pk):
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return HttpResponseNotFound("Song does not exist")

    mood_query = request.GET.get('mood')
    genre_query = request.GET.get('genre')
    favourite_query = request.GET.get('favourite')
    following_query = request.GET.get('following')

    #  determine next song according to the query_string
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

    # store values in session for further use
    request.session['next_song_id'] = next_song.id
    request.session['current_song_id'] = pk
    request.session['query_string'] = query_string

    comments = Comment.objects.filter(song=song)
    comment_form = CommentForm()  # form for create-comment

    context = {
        "song": song,
        "next_song": next_song,
        "previous_song": previous_song,
        "comments": comments,
        "comment_form": comment_form,
        "query_string": query_string
    }

    return render(request, 'songs/song_detail.html', context=context)


def song_detail_action(request, pk):
    if not request.user.is_authenticated:
        # If user is not login, redirect to login-screen
        return JsonResponse({"status": "false", 'message': 'User is not authenticated'}, status=403)

    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return HttpResponseNotFound("Song does not exist")

    if request.method == "POST":
        # create comment
        data = json.loads(request.body)
        comment_form = CommentForm(data)
        if comment_form.is_valid():
            temp = comment_form.save(commit=False)
            temp.owner = request.user
            temp.song = song
            temp.save()

            return JsonResponse(temp.serialize())

    if request.method == "PUT":
        # favourite-unfavourite action
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
        return JsonResponse(response)


def comment_action(request, pk):
    # delete comment
    if request.method == "DELETE":
        comment = Comment.objects.get(pk=pk)
        comment.delete()

        response = {
            "status": "OK"
        }
        return JsonResponse(response)

    # edit comment
    if request.method == "PUT":
        data = json.loads(request.body)
        # print(data)
        comment_text = data.get('comment_text')
        comment = Comment.objects.get(pk=pk)
        comment.text = comment_text
        comment.save()

        response = {
            "status": "OK"
        }
        return JsonResponse(response)
