from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('songs/', views.SongListView.as_view(), name='songs'),
    path('artists/', views.ArtistListView.as_view(), name='artists'),
    path('artists/<int:artist_id>/', views.ArtistSongView.as_view(), name='artist-songs'),
    path('moods/', views.MoodListView.as_view(), name='moods'),
    path('moods/<int:mood_id>/', views.MoodSongView.as_view(), name='mood-songs'),
    path('favourite/', views.favourite, name='favourite'),
]
