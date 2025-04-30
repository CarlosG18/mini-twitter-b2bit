from mini_twitter.models import User, Post, Follow
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

    # aplicando as validações nos dados enviados
    

class PostSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']

    # aplicando as validações nos dados enviados

"""
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []

    # aplicando as validações nos dados enviados
"""