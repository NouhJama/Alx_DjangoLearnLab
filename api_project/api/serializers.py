from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields of the Book model

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__' # Serialize all fields of the Author model       