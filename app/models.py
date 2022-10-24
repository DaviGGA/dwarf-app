from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser




class Profile (models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 16, blank = True)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profile_img = models.ImageField(default = 'blank-profile-picture.png', upload_to = 'profile_images')

    def __str__(self):
        return self.user.username
