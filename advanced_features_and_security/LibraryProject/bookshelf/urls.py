"""
URL configuration for bookshelf app.
Maps URLs to permission-protected views for book operations.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Function-based views with permission decorators
    path('books/', views.book_list_view, name='book_list'),
    path('books/create/', views.book_create_view, name='book_create'),
    path('books/<int:book_id>/edit/', views.book_edit_view, name='book_edit'),
    path('books/<int:book_id>/delete/', views.book_delete_view, name='book_delete'),
    
    # Class-based views with permission mixins (alternative implementation)
    path('books/cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('books/cbv/create/', views.BookCreateView.as_view(), name='book_create_cbv'),
    path('books/cbv/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit_cbv'),
    path('books/cbv/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete_cbv'),
]