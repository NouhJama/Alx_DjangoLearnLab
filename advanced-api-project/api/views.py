from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Author, Book
from .serializers import  BookSerializer
from rest_framework import permissions

# Create your views here.
# View for listing and creating Books
class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            """
            Only authenticated users can create a new Book
            -GET (list) is open to all users
            -POST (create) requires authentication
            """
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

# View for retrieving, updating, and deleting a Book
class BookRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            """
            Only authenticated users can update or delete a Book
            -GET (retrieve) is open to all users
            -PUT, PATCH, DELETE require authentication
            """
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
