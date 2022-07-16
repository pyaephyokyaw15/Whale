from .models import Mood, Genre


def song_filter(request):
    moods = Mood.objects.all()
    genres = Genre.objects.all()
    return {'moods': moods, 'genres': genres}


