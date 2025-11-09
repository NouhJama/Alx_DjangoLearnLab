from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Library, Book, Author, Librarian

# Create your views here.

# Function-based view.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

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
    

