from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import CustomUser, Post, Comment

# Custom permissions only logged-in users can create posts/comments
class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

# Custom permission to allow only owner to edit or delete their objects(posts/comments)
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the post/comment.
        return obj == request.user
    
