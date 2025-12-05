from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views    

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(template_name='blog/register.html'), name='register'),
    path('profile/', views.profile, name='profile'),

    # CRUD URL patterns for Post model
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Include comment URLs
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

]