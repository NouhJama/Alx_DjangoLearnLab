from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserRegistrationView, LoginView, PostViewSet, CommentViewSet, ProfileViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'profile', ProfileViewSet, basename='profile')



urlpatterns = [
    path("login/", LoginView.as_view(), name="api_token_auth"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("auth/api/", ObtainAuthToken.as_view(), name="api_token_auth"),

]

urlpatterns += router.urls