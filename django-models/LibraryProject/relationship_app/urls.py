from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books

urlpatterns = [
    # Function-based view
    path('books/function/', views.list_books, name='list-books-function'),
    
    # Class-based ListView pattern
    path('books/', views.BookListView.as_view(), name='book-list'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-specific views
    path('admin/', views.admin_view.as_view(), name='admin-view'),
    path('librarian/', views.librarian_view.as_view(), name='librarian-view'),
    path('member/', views.member_view.as_view(), name='member-view'),
]