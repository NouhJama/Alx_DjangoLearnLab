from .views import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import path, include

urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
]
