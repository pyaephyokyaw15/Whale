from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('', views.SongListView.as_view(), name='songs'),
    path('songs/', views.SongListView.as_view(), name='songs'),
    path('songs/<int:song_id>/', views.song, name='song'),
    path('artists/', views.ArtistListView.as_view(), name='artists'),
    path('artists/<int:artist_id>/', views.artist_songs, name='artist-songs'),
    path('artists/<int:artist_id>/<int:song_id>', views.artist_songs_song, name='artist-songs-song'),
    path('moods/', views.MoodListView.as_view(), name='moods'),
    path('moods/<int:mood_id>/', views.mood_songs, name='mood-songs'),
    path('moods/<int:mood_id>/<int:song_id>', views.mood_songs_song, name='mood-songs-song'),
    path('moods/route/<int:mood_id>/<int:song_id>', views.mood_route, name='mood-route'),
    path('favourite/', views.favourite, name='favourite'),
    path('favourite/<int:song_id>/', views.favourite_songs_song, name='favourite-songs-song'),
    path('edit/<int:song_id>/', views.edit, name='edit'),   
]
