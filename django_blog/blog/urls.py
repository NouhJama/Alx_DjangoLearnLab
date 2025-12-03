from django.urls import path
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register', template_name='blog/registration.html'),
    path('profile/', views.profile, name='profile', template_name='blog/profile.html'),
    path('', views.home, name='blog-home'),
]