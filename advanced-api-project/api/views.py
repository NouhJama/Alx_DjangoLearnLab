from django.shortcuts import render
from rest_framework import generics
from .models import Author, Book
from .serializers import  BookSerializer
from rest_framework import permissions

# Create your views here.
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]