from django.shortcuts import render, redirect
from songs.models import Song
from django.conf import settings
from .forms import UserRegisterForm, ProfileForm
from django.http import HttpResponse, HttpResponseNotFound
from accounts.models import User
# Create your views here.
def profile(request, username):
    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return HttpResponseNotFound("User does not exist")



    songs = Song.objects.filter(owner=user)
    favourite_songs = Song.objects.filter(favourite_by=request.user).all()
    uploaded_songs = Song.objects.filter(owner=request.user).all()

    context = {
        "songs": songs,
        'following_counts': user.following.count,
        'follower_counts': user.followers.count,
        "favourite_songs": favourite_songs,
        "uploaded_songs": uploaded_songs
    }
    return render(request, 'accounts/profile.html', context=context)




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def profile_change(request, username):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        print(form.errors)
        if form.is_valid():
            form.save()

    else:
        form = ProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_change.html', context)
