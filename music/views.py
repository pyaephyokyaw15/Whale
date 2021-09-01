from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Song


# Create your views here.
def index(request):
    s1 = Song.objects.get(pk=1)
    return HttpResponse(s1.title)
