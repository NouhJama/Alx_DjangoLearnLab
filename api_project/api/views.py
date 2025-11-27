from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from .serializers import BookSerializer, AuthorSerializer, UserProfileSerializer
from .models import Book, User, UserProfile, Author



# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Require authentication to access this viewset

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() # Get all Book records
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser] # Require authentication to access this viewset

# Add UserProfile views
class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the UserProfile
        serializer.save(user=self.request.user)  