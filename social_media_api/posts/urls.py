from rest_framework import routers
from .views import PostViewSet, CommentViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path("", include(router.urls)),
]
