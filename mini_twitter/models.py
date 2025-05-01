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

class UserTwitter(models.Model):
    """
        class for user
        - user is a OneToOneField to the User model from django
        - created_at is a DateTimeField that stores the date and time when the user was created
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
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    body = models.TextField()
    status = models.IntegerField(choices=StatusEnum.choices(), default=StatusEnum.ACTIVE.value)
    created_at = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    
    def __str__(self):
        return self.title