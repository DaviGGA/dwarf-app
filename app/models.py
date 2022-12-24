from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime




 
class Profile (models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 16, blank = True)
    first_name = models.CharField(max_length=16, blank= True)
    last_name = models.CharField(max_length=16, blank= True)
    bio = models.TextField(blank = True)
    profile_img = models.ImageField(default = 'blank-profile-picture.png', upload_to = 'profile_images')

    def __str__(self):
        return self.user.username
    

class Follow(models.Model):
    following = models.ForeignKey(Profile, on_delete= models.CASCADE)
    followed = models.ManyToManyField(Profile, related_name = "follows", blank = True)

    def __str__(self):
        return f"{self.following}"

    def following_count(self):
        return self.followed.all().count()
    
    def followers_count(self):      
        return self.following.follows.all().count()
    
    
        

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


class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    posted_at = models.DateTimeField()
    text_content = models.TextField(max_length=280)

    def __str__(self):
        return f"{self.post.profile.user.username} | {self.text_content[:15]}..."



class Like (models.Model):
    who_is_liking = models.CharField(max_length=100, blank=False, null = False)
    post_being_liked = models.CharField(max_length=100, blank=False, null = False)
