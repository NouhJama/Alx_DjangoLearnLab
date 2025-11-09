from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    # Function-based view
    path('books/function/', views.list_books, name='list-books-function'),
    
    # Class-based ListView patterns
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    
    # Class-based DetailView patterns
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]