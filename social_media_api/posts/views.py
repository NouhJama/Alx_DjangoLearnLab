from django.shortcuts import render
from .models import Post, Comment, Like
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from posts.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from .pagination import DefaultPagination
from notifications.models import Notification


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    # Filtering and searching 
    filter_backends = [SearchFilter, DjangoFilterBackend]

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
class LikePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create notification for post author
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'status': 'post liked'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'you already liked this post'}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'status': 'you have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)