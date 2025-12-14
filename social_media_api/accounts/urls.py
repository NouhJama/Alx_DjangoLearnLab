from .views import UserRegistrationView, LoginView, ProfileViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
]

urlpatterns += router.urls