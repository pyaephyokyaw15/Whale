from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # add class to default html tags created by django
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # add class to default html tags created by django
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # override the default login error message
        self.error_messages['invalid_login'] = 'Invalid username or password'
        # add class to default html tags created by django
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
