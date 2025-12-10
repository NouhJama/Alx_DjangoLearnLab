from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserRegistrationView, loginView
from django.urls import path

urlpatterns = [
    path("login/", ObtainAuthToken, name="api_token_auth"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
]