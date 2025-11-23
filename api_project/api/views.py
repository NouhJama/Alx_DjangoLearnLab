from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from .serializers import BookSerializer
from .models import Book



# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Require authentication to access this viewset

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() # Get all Book records
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser] # Require authentication to access this viewset