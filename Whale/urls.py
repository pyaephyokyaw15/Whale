"""Whale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('music.urls')),
    path('admin/', admin.site.urls),
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.register, name='register'), 

    # We can leave templave_name in logout. 
    # If so, it will logout and when we login again, it will take to admin login.
    # Not user login.
    # So, to get customize, we create logout.html.
    path('logout/', user_views.user_logout, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

