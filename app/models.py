from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime




class Profile (models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 16, blank = True)
    first_name = models.CharField(max_length=16, blank= True)
    last_name = models.CharField(max_length=16, blank= True)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profile_img = models.ImageField(default = 'blank-profile-picture.png', upload_to = 'profile_images')

    def __str__(self):
        return self.user.username


class Post (models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete= models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank = True, null = True)
    text_content = models.TextField(max_length=280)
    posted_at = models.DateTimeField()
    likes = models.IntegerField(default=0)
    reposts = models.IntegerField(default=0)
    coments = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.profile.user.username} | {self.text_content[:15]}..."



class Follow (models.Model):
    who_is_following = models.CharField(max_length=100, blank=False, null=False)
    who_is_being_followed = models.CharField(max_length=100, blank=False, null=False)

class Like (models.Model):
    who_is_liking = models.CharField(max_length=100, blank=False, null = False)
    post_being_liked = models.CharField(max_length=100, blank=False, null = False)