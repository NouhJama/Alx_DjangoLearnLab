from rest_framework import routers
from .views import PostViewSet, CommentViewSet, LikePostViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'like', LikePostViewSet, basename='likepost')

urlpatterns = [
    path("", include(router.urls)),
]
