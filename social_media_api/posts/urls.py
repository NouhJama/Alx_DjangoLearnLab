from rest_framework import routers
from .views import PostViewSet, CommentViewSet, LikePostView, UnlikePostView, FollowView, UnfollowView
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path("", include(router.urls)),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('follow/<int:pk>/', FollowView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', UnfollowView.as_view(), name='unfollow-user'),
]
