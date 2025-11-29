from .views import BookListCreateView, BookRetrieveUpdateDestroyView
from django.urls import path, include

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
