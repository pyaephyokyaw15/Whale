from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('setting/', views.setting, name='setting'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('user/<str:username>', views.profile, name='profile'),
]