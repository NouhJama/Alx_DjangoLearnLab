# Query all books by specific author
from relationship_app.models import Author, Book, Library, Librarian
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)

# List all books in the library
books = Library.objects.get(name='Central Library').books.all()

# Retrieve the librarian of a specific library
def get_librarian_of_library(library_name):
    return Librarian.objects.get(name=library_name)