from rest_framework import routers
from django.urls import path, include
from .views import UserTwitterViewSet, PostViewSet, FollowToggleView, FeedView

router = routers.DefaultRouter()

# registrando as rotas das views
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/registration/', UserTwitterViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-detail'),
    path('users/follow/<int:pk>/', FollowToggleView.as_view(), name='follow-toggle'),
    path('feed/', FeedView.as_view(), name='feed'),
]