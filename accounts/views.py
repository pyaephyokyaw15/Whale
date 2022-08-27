from django.shortcuts import render, redirect
from songs.models import Song
from .forms import UserRegisterForm, ProfileForm
from django.http import HttpResponseNotFound
from accounts.models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
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


@login_required()
def setting(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=request.user.username)

    else:
        form = ProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/setting.html', context)


def profile(request, username):
    current_user = request.user

    if request.method == "GET":
        profile_user = get_object_or_404(User, username=username)
        favourite_songs = Song.objects.filter(favourite_by=profile_user).all()
        uploaded_songs = Song.objects.filter(owner=profile_user).all()

        # determine follow button visibility
        print(current_user)
        print(profile_user)
        follow_button_visibility = current_user != profile_user

        # follow-unfollow state
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

    # follow-unfollow action
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

        return JsonResponse(response)
