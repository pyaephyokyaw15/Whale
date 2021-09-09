from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('songs')
            
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid Username or Password'})
    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return redirect ('songs')
