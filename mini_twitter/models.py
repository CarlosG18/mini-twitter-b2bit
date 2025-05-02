from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from enum import Enum

class StatusEnum(Enum):
    """
        - Enum for status´s type
            1. ACTIVE -> post is active and can be seen by other users
            2. INACTIVE -> post is inactive and can not be seen by other users
    """
    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def choices(cls):
        return [(i.value, i.name) for i in cls]

    @classmethod
    def get_name(cls, value):
        return cls(value).name
    
class Hastag(models.Model):
    """
        class for hastag
        - name is a CharField that stores the name of the hastag
    """
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class UserTwitter(models.Model):
    """
        class for user
        - user is a OneToOneField to the User model from django
        - created_at is a DateTimeField that stores the date and time when the user was created
        - followers is a ManyToManyField to the UserTwitter model that stores the followers of the user
        - following is a ManyToManyField to the UserTwitter model that stores the users that the user is following
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_following')
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_followers')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    """
        class for post
        - title is a CharField that stores the title of the post
        - body is a TextField that stores the body of the post
        - status is a IntegerField that stores the status of the post
        - created_at is a DateTimeField that stores the date and time when the post was created
        - user_twitter is a ForeignKey to the UserTwitter model that stores the user that created the post
        - likes is a IntegerField that stores the number of likes of the post
        - likes_users is a ManyToManyField to the UserTwitter model that stores the users that liked the post
        - hastags is a ManyToManyField to the Hastag model that stores the hastags of the post
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    body = models.TextField()
    status = models.IntegerField(choices=StatusEnum.choices(), default=StatusEnum.ACTIVE.value)
    created_at = models.DateTimeField(default=datetime.now())
    user_twitter = models.ForeignKey(UserTwitter, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    likes_users = models.ManyToManyField(UserTwitter, related_name='likes', blank=True)
    hastags = models.ManyToManyField(Hastag, blank=True, related_name='posts')

    @property
    def count_likes(self):
        """
            - count the number of likes
        """
        return self.likes.count()
    
    def __str__(self):
        return self.title