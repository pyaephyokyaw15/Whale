from django.urls import path
from . import views

app_name = 'songs'

urlpatterns = [
    path('', views.SongListView.as_view(), name='all_songs'),
    path('favourites/', views.FavouriteSongListView.as_view(), name='favourite_songs'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genres/<slug:slug>/', views.GenreSongListView.as_view(), name='genre_songs'),
    path('moods/', views.MoodListView.as_view(), name='moods'),
    path('moods/<slug:slug>/', views.MoodSongListView.as_view(), name='mood_songs'),
]