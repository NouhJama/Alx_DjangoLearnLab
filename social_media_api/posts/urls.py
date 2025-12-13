from rest_framework import routers
from .views import PostViewSet, CommentViewSet, LikePostViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path("", include(router.urls)),
    path('posts/<int:pk>/like/', LikePostViewSet.as_view({'post': 'like'}), name='like-post'),
    path('posts/<int:pk>/unlike/', LikePostViewSet.as_view({'post': 'unlike'}), name='unlike-post'),
]
