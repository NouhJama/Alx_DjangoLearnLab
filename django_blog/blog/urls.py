from django.urls import path
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register', template_name='blog/registration.html'),
    path('profile/', views.profile, name='profile', template_name='blog/profile.html'),

    # CRUD URL patterns for Post model
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
]