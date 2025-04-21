from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
# Create your models here.

# Profile model - contains user, id_user, bio, profileimg, location
# Return username of user
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)
    bio = models.TextField(blank=True, default='')
    profileimg = models.ImageField(upload_to='profile_images', default='user.png')
    location = models.CharField(max_length=80, blank=True, default='')

    def __str__(self):
        return self.user.username

# Post model - contains unique_id, image, caption, time created, likes
# Return user who posted 
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images', null=True, blank=True, default='user.png')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    numLikes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
# LikePost model - contains post_id and username of user who liked the post
# Return username of user who liked the post
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
# Followers model - contains follower and user
# Return user who followed
class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user