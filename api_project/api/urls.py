from django.urls import path, include
from .views import BookList, BookViewSet, UserProfileList, UserProfileViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('profiles_all/', UserProfileList.as_view(), name='userprofile-list'),
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'), # obtain auth token by posting username and password 
]