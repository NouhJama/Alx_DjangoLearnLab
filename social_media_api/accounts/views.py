from django.shortcuts import render
import accounts
from posts.permissions import IsOwnerOrReadOnly
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets
from .serializers import UserCreateSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from accounts.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
# Create your views here.
from .serializers import UserCreateSerializer, UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
    
# Follow and Unfollow functionality
class FollowView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can follow/unfollow                                        

    def post(self, request, pk):
        try:
            target_user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Prevent users from following/unfollowing themselves
        if target_user == request.user:
            return Response({'error': 'You cannot follow/unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if request.user.following.filter(id=target_user.id).exists():
            # Return 'You are already following this user'
            return Response({'status': 'You are already following this user.'}, 
                            status=status.HTTP_400_BAD_REQUEST
                            )
        # Add target_user to the following list of the request.user
        request.user.following.add(target_user)
        return Response({'status': 'User followed successfully.'}, 
                        status=status.HTTP_200_OK
                        )
# Unfollow functionality
class UnfollowView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can follow/unfollow                                        

    def post(self, request, pk):
        try:
            target_user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Prevent users from following/unfollowing themselves
        if target_user == request.user:
            return Response({'error': 'You cannot follow/unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following and unfollow
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
            return Response({'status': 'User unfollowed successfully.'}, 
                            status=status.HTTP_200_OK
                            )
        return Response({'status': 'You are not following this user.'}, 
                        status=status.HTTP_400_BAD_REQUEST
                        )
    
