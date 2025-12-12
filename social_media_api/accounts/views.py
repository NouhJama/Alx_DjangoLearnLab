from django.shortcuts import render
from .models import CustomUser, Post, Comment
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
# import modelviewsets for posts and comments
from rest_framework import viewsets


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        user = serializer.validated_data.get('user')
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "token": token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Post creation and management using ModelViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comment creation and management using ModelViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ViewSet for the profile management.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()