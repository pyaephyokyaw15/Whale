from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(default='images/profiles/default.png', upload_to='images/profiles/')
    authentic = models.BooleanField(default=False)  # give blue-mark for authentic user, defined by admin
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.username

    @property
    def following(self):
        return User.objects.filter(followers=self)



