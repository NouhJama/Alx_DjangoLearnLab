from django.shortcuts import render
from .models import Post, Comment, Like
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from posts.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from .pagination import DefaultPagination


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    # Filtering and searching 
    filter_backends = ['SearchFilter', 'DjangoFilterBackend']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Like and Unlike functionality
class LikePostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def like_post(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'status': 'post liked'})
        return Response({'status': 'post already liked'}, status=status.HTTP_400_BAD_REQUEST)   

    def unlike_post(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        post.likes.remove(request.user)
        post.save()
        return Response({'status': 'post unliked'})