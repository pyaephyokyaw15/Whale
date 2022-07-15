from django.shortcuts import render
from songs.models import Song


# Create your views here.
def profile(request):
    songs = Song.objects.filter(owner=request.user)

    context = {
        "songs": songs
    }
    return render(request, 'accounts/profile.html', context=context)
