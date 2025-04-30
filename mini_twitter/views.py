from .serializers import UserSerializer, PostSerializer
from .models import User, Post
from rest_framework import viewsets

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    