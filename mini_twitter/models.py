from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from enum import Enum

class RoleEnum(Enum):
    """
        - Enum for list types of Role
            1. ADMIN
            2. USER
    """
    pass

class StatusEnum(Enum):
    """
        - Enum for status´s type
            1. 
            2. 
    """
    pass

# Create your models here.
class User(models.Model):
    """
        
    """

    username = models.CharField(max_length=255)
    role = models.IntegerField()

    def __str__(self):
        return super().__str__()

class Post(models.Model):
    """
    
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    #status
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return super().__str__()

class Follow(models.Model):
    """
    
    """
    pass

    def __str__(self):
        return super().__str__()