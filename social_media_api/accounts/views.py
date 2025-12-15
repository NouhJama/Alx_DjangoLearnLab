from django.shortcuts import render

import accounts
from posts.permissions import IsOwnerOrReadOnly
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserCreateSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from accounts.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly


# Create your views here.
from .serializers import UserCreateSerializer, UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Token is already created in serializer

        # Return user data with clean UserSerializer (for response)
        user_data = UserSerializer(user, context={'request': request}).data
        token = Token.objects.get(user=user)

        return Response({
            "user": user_data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)

        # Return user info using UserSerializer
        user_data = UserSerializer(user, context={'request': request}).data

        return Response({
            "message": "Login successful",
            "user": user_data,
            "token": token.key
        }, status=status.HTTP_200_OK)


# ViewSet for the profile management.
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
    
