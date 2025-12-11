from django.contrib import admin
from .models import CustomUser, Post, Comment
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'birth_date')
    search_fields = ('username', 'email')
    fieldsets = (
        ( 'Login Info', {'fields': ('username', 'password', 'email')}),
        ('Personal Info', {'fields': ('bio', 'birth_date', 'profile_picture')}),
        ('Social Info', {'fields': ('followers',)}),
        )
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('author__username', 'content', 'post__content')
    list_filter = ('created_at',)