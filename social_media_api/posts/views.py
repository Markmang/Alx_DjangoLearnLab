from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Like
from notifications.utils import create_notification



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners to edit/delete their objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the owner
        return obj.author == request.user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class FeedView(generics.ListAPIView):
    """
    Returns posts from users the current user follows, newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        user = self.request.user
        # If user follows nobody, return empty queryset
        following_users = user.following.all()
        if not following_users.exists():
            return Post.objects.none()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

from rest_framework.views import APIView

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        create_notification(recipient=post.author, actor=user, verb='liked your post', target=post)
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        deleted, _ = Like.objects.filter(post=post, user=user).delete()
        if not deleted:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
