from django.shortcuts import render, redirect
from songs.models import Song
from django.conf import settings
from .forms import UserRegisterForm, ProfileForm
from django.http import HttpResponse, HttpResponseNotFound
from accounts.models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView

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


class ProfileUpdateView(UpdateView):
    # specify the model you want to use
    model = User

    # specify the fields
    fields = [
        "first_name",
        "last_name",
        "profile_picture"
    ]

    # can specify success url
    # url to redirect after successfully
    # updating details
    template_name = 'accounts/setting.html'


def setting(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        print(form.errors)

        if form.is_valid():
            form.save()

    else:
        form = ProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/setting.html', context)


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