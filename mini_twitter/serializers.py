from mini_twitter.models import UserTwitter, Post
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer for Django's built-in User model.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # aplicando as validações nos dados enviados

class UserTwitterSerializer(serializers.ModelSerializer):
    """
        Serializer for the UserTwitter model.
    """
    user = UserSerializer()

    class Meta:
        model = UserTwitter
        fields = ['user', 'created_at', 'followers', 'following']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'followers': {'read_only': True},
            'following': {'read_only': True}
        }

    # aplicando as validações nos dados enviados
    

class PostSerializer(serializers.ModelSerializer):
    """
        Serializer for the Post model.
    """

    class Meta:
        model = Post
        fields = ['id', 'title', 'body','image', 'likes', 'status', 'created_at', 'likes_users']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'likes': {'read_only': True},
            'status': {'read_only': True},
            'likes_users': {'read_only': True}
        }

    # aplicando as validações nos dados enviados
