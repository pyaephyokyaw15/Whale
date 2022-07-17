from django.urls import path
from . import views

app_name = 'songs'

urlpatterns = [
    path('', views.SongListView.as_view(), name='all_songs'),
    path('search/', views.SongSearchView.as_view(), name='search'),
    path('<int:pk>/', views.song_detail, name='song_detail'),
    path('<int:pk>/action/', views.song_action, name='song_action'),
    path('favourites/', views.FavouriteSongListView.as_view(), name='favourite_songs'),
    path('genres/<slug:slug>', views.GenreSongListView.as_view(), name='genre_songs'),
    path('moods/<slug:slug>', views.MoodSongListView.as_view(), name='mood_songs'),
    path('upload/', views.SongUploadView.as_view(), name='upload'),
]