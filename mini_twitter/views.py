from .serializers import UserTwitterSerializer, PostSerializer
from .models import UserTwitter, Post
from .pagination import FeedPagination

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

def get_message_response(flag, message, status_code, data=None):
    """
        Generate a standardized response message for API views.

        This function returns a dictionary with a consistent structure for success or error responses.

        Args:
            flag (str): Indicates the type of response ('success' or 'error').
            message (str): A descriptive message to include in the response.
            status_code (int): The HTTP status code to return.
            data (dict or None, optional): Additional data to include in success responses.

        Returns:
            dict: A structured response containing the status, code, message, and optionally data.
    """
    if flag == 'success':
        return {
            'status': 'success',
            'code': status_code,
            'message': message,
            'data': data
        }
    elif flag == 'error':
        return {
            'status': 'error',
            'code': status_code,
            'message': message
        }

class UserTwitterViewSet(viewsets.ModelViewSet):
    """
        ViewSet for managing `UserTwitter` instances.

        This ViewSet allows for listing, retrieving, creating, and updating UserTwitter objects.
        It uses `JWT authentication` and requires authenticated access for most actions,
        except for the **create** action, which allows unauthenticated access to register new users.
    """
    queryset = UserTwitter.objects.all()
    serializer_class = UserTwitterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            # Allow unauthenticated users to create a new user
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
            Create a new user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(get_message_response('success', 'User created successfully', 201, serializer.data), status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        try:
            # check if the user already exists
            user = User.objects.get(username=serializer.validated_data['user']['username'])
            return Response(get_message_response('error', 'User already exists', 400), status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # create a new user
            user = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user)
            serializer.save(user=user)

class FollowToggleView(APIView):
    """
        API view to follow or unfollow a user.

        This view allows authenticated users to toggle the follow status of another user.
        JWT authentication is required to access this endpoint.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, pk=None):
        """
            Toggle the follow status for a target user.

            If the authenticated user is already following the specified user (by pk), this will unfollow them.
            If not, it will initiate a follow. A user cannot follow themselves.

            Args:
                request (HttpRequest): The HTTP request with the authenticated user.
                pk (int): The primary key of the user to follow or unfollow.

            Returns:
                Response: A success or error response with a message and updated user data if applicable.
        """
        try:
            # check if the user already exists
            user = UserTwitter.objects.get(user=request.user)

            # check if the user to follow exists and is not the same as the current user
            if pk == user.pk:
                return Response(get_message_response('error', 'You cannot follow yourself', 400), status=status.HTTP_400_BAD_REQUEST)
            else:
                user_to_follow = UserTwitter.objects.get(pk=pk)

            # check if the user_to_follow is already following the user
            if user_to_follow in user.following.all():
                # unfollow the user
                user.following.remove(user_to_follow)
                user_to_follow.followers.remove(user)
                user_to_follow.save()
                user.save()
                data_user = UserTwitterSerializer(user).data
                return Response(get_message_response('success', 'User unfollowed successfully', 200, data_user), status=status.HTTP_200_OK)
            else:
                # follow the user
                user.following.add(user_to_follow)
                user_to_follow.followers.add(user)
                user_to_follow.save()
                user.save()
                data_user = UserTwitterSerializer(user).data
                return Response(get_message_response('success', 'User followed successfully', 200, data_user), status=status.HTTP_200_OK)
        except UserTwitter.DoesNotExist:
            return Response(get_message_response('error', 'User does not exist', 400), status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
    """
        ViewSet for managing user posts.

        Provides endpoints for creating, listing, updating, deleting, and liking posts.
        All actions require authentication using JWT tokens.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
            Get the posts of the user
        """
        user = UserTwitter.objects.get(user=self.request.user)
        return Post.objects.filter(user_twitter=user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
            list all posts of the user
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Pagination
        paginator = FeedPagination()
        paginated_posts = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(get_message_response('success', 'Posts retrieved successfully', 200, serializer.data))
    
    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # check post exists in the queryset
        try:
            post = queryset.get(pk=kwargs['pk'])
        except Post.DoesNotExist:
            return Response(get_message_response('error', 'Post does not exist', 400), status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # check if the post is updated
        if serializer.instance:
            return Response(get_message_response('success', 'Post updated successfully', 200, serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(get_message_response('error', 'Post not updated', 400), status=status.HTTP_400_BAD_REQUEST)
        
    def perform_update(self, serializer):
        """
            Save the post
        """
        serializer.save(user_twitter=UserTwitter.objects.get(user=self.request.user))
    
    def destroy(self, request, *args, **kwargs):
        """
            Delete a post
        """
        queryset = self.get_queryset()
        # check post exists in the queryset
        try:
            post = queryset.get(pk=kwargs['pk'])
        except Post.DoesNotExist:
            return Response(get_message_response('error', 'Post does not exist', 400), status=status.HTTP_400_BAD_REQUEST)
        
        post.delete()
        return Response(get_message_response('success', 'Post deleted successfully', 200), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            Create a new post
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        """
            Save the post
        """
        serializer.save(user_twitter=UserTwitter.objects.get(user=self.request.user))

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
            Toggle like or unlike for a specific post.

            If the user has already liked the post, it will be unliked.
            If not, it will be liked.

            Args:
                pk (int): The primary key of the post to like or unlike.

            Returns:
                Response: A message indicating whether the post was liked or unliked.
        """
        try:
            post = self.get_object()
            user = UserTwitter.objects.get(user=request.user)
            if user in post.likes_users.all():
                # unlike the post
                post.likes_users.remove(user)
                post.likes -= 1
                post.save()
                data_post = PostSerializer(post).data
                return Response(get_message_response('success', 'Post unliked successfully', 200, data_post), status=status.HTTP_200_OK)
            else:
                # like the post
                post.likes_users.add(user)
                post.likes += 1
                post.save()
                data_post = PostSerializer(post).data
                return Response(get_message_response('success', 'Post liked successfully', 200, data_post), status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(get_message_response('error', 'Post does not exist', 400), status=status.HTTP_400_BAD_REQUEST)
    
class FeedView(APIView):
    """
       API view to retrieve the feed of posts from followed users.

        This view allows authenticated users to fetch posts from users they follow, with pagination.
        JWT authentication is required for access.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
            Retrieve the feed of posts from users followed by the authenticated user.

            The posts are ordered by creation date (newest first) and are paginated.

            Returns:
                Response: A paginated list of posts from users the authenticated user is following.
        """
        user_current = UserTwitter.objects.get(user=request.user)
        posts = Post.objects.filter(user_twitter__in=user_current.following.all()).order_by('-created_at')

        # Pagination
        paginator = FeedPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(get_message_response('success', 'Feed retrieved successfully', 200, serializer.data))