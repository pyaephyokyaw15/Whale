from django.shortcuts import render, redirect
from songs.models import Song
from django.conf import settings
from .forms import UserRegisterForm, ProfileForm
from django.http import HttpResponse, HttpResponseNotFound
from accounts.models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def profile(request, username):
    current_user = request.user
    if request.method == "GET":
        try:
            profile_user = User.objects.get(username=username)

        except User.DoesNotExist:
            return HttpResponseNotFound("User does not exist")

        favourite_songs = Song.objects.filter(favourite_by=profile_user).all()
        uploaded_songs = Song.objects.filter(owner=profile_user).all()

        # determine follow button visibility
        print(current_user)
        print(profile_user)
        follow_button_visibility = current_user != profile_user

        if current_user in profile_user.followers.all():
            status = "Unfollow"
        else:
            status = "Follow"

        context = {
            'profile_user': profile_user,
            'following_counts': profile_user.following.count,
            'follower_counts': profile_user.followers.count,
            "favourite_songs": favourite_songs,
            "uploaded_songs": uploaded_songs,
            "follow_button_visibility": follow_button_visibility,
            "status": status,
        }
        return render(request, 'accounts/profile.html', context=context)


    elif request.method == "PUT":
        try:
            profile_user = User.objects.get(username=username)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        data = json.loads(request.body)
        print(data)

        following_status = data.get("followingStatus")

        if following_status == 'Unfollow':
            profile_user.followers.remove(current_user)
            status = "Follow"

        elif following_status == 'Follow':
            profile_user.followers.add(current_user)
            status = "Unfollow"

        profile_user.save()

        response = {
            "followingStatus": status,
            'following_counts': profile_user.following.count(),
            'follower_counts': profile_user.followers.count(),

        }

        print("Hay It is OK")
        print(response)
        return JsonResponse(response)