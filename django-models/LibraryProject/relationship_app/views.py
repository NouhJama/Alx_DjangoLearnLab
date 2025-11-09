from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView
from relationship_app.models import Book, Author, Library, Librarian

# Create your views here.

# Function-based view (your original)
def list_books(request):
    books = Book.objects.all()
    for book in books:
        return f"Book: {book.title}, Author: {book.author.name}"

# Class-based view for displaying a specific library details, listing all its books and librarian
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        context['librarian'] = library.librarian
        return context
    

