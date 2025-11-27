from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Author, UserProfile

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields of the Book model

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__' # Serialize all fields of the Author model

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Serialize selected User fields

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    # Custom fields
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'bio', 'phone_number', 'date_of_birth']  # Serialize these fields

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()     