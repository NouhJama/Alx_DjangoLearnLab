# Query all books by specific author
from relationship_app.models import Author, Book, Library, Librarian
def get_books_by_author(author_name):
    return Book.objects.filter(name=author_name)

# List all books in a library
def get_books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

# Retrieve the librarian of a specific library
def get_librarian_of_library(library_name):
    return Librarian.objects.get(name=library_name)