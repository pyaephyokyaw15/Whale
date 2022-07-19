from django.urls import path
from . import views

app_name = 'songs'

urlpatterns = [
    path('', views.SongListView.as_view(), name='songs'),
    path('<int:pk>/action/', views.song_detail_action, name='song_detail_action'),
    path('<int:pk>/', views.song_detail, name='song_detail'),
    path('upload/', views.SongUploadView.as_view(), name='upload'),
]