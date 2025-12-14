from django.contrib import admin
from .models import Post, Comment, Like
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'updated_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'updated_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    search_fields = ('user__username', 'post__content')


