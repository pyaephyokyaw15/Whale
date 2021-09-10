from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('', views.SongListView.as_view(), name='songs'),
    path('songs/', views.SongListView.as_view(), name='songs'),
    path('songs/<int:song_id>/', views.song, name='song'),
    path('songs/next/<int:song_id>', views.song_next, name='song-next'),
    path('songs/prev/<int:song_id>', views.song_prev, name='song-prev'),
    path('artists/', views.ArtistListView.as_view(), name='artists'),
    path('artists/<int:artist_id>/', views.artist_songs, name='artist-songs'),
    path('artists/<int:artist_id>/<int:song_id>', views.artist_songs_song, name='artist-songs-song'),
    path('artists/next/<int:artist_id>/<int:song_id>', views.artist_next, name='artist-next'),
    path('artists/prev/<int:artist_id>/<int:song_id>', views.artist_prev, name='artist-prev'),
    path('moods/', views.MoodListView.as_view(), name='moods'),
    path('moods/<int:mood_id>/', views.mood_songs, name='mood-songs'),
    path('moods/<int:mood_id>/<int:song_id>', views.mood_songs_song, name='mood-songs-song'),
    path('moods/next/<int:mood_id>/<int:song_id>', views.mood_next, name='mood-next'),
    path('moods/prev/<int:mood_id>/<int:song_id>', views.mood_prev, name='mood-prev'),
    path('favourite/', views.favourite, name='favourite'),
    path('favourite/<int:song_id>/', views.favourite_songs_song, name='favourite-songs-song'),
    path('favourite/next/<int:song_id>', views.favourite_next, name='favourite-next'),
    path('favourite/prev/<int:song_id>', views.favourtie_prev, name='favourite-prev'),
    path('edit/<int:song_id>/', views.edit, name='edit'),
    
]
