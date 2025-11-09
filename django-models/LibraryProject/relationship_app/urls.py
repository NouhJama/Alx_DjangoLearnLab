from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    # Function-based view
    path('books/function/', views.list_books, name='list-books-function'),
    
    # Class-based ListView pattern
    path('books/', views.BookListView.as_view(), name='book-list'),

    # Authentication views
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]