from django.contrib import admin
from .models import CustomUser
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
    
