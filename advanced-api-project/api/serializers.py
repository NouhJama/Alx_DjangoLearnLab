from rest_framework import serializers
from .models import Author, Book
from datetime import date

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

    # Custom field validation: publication_year cannot be in the future
    def validate_publication_year(self, value):
        if value.year > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Nested serializer for Author including their books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, source='book_set')

    class Meta:
        model = Author
        fields = ['name', 'books']
