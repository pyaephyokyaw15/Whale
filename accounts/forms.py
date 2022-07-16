from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

