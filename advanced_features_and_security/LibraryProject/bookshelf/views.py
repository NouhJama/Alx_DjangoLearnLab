from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Book

# Permission-based function views with proper permission checks
# These views use the custom permissions: can_view, can_create, can_edit, can_delete

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list_view(request):
    """
    View to list all books - requires 'can_view' permission.
    Users must be in a group with 'can_view' permission to access this view.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create_view(request):
    """
    View to create a new book - requires 'can_create' permission.
    Only users with 'can_create' permission can add new books.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            Book.objects.create(
                title=title,
                author=author,
                publication_year=int(publication_year)
            )
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit_view(request, book_id):
    """
    View to edit an existing book - requires 'can_edit' permission.
    Only users with 'can_edit' permission can modify existing books.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = int(request.POST.get('publication_year', book.publication_year))
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete_view(request, book_id):
    """
    View to delete a book - requires 'can_delete' permission.
    Only users with 'can_delete' permission can remove books.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Class-based views with permission mixins for alternative implementation
class BookListView(PermissionRequiredMixin, ListView):
    """
    Class-based view to list books with permission requirement.
    Demonstrates using PermissionRequiredMixin with generic views.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'

class BookCreateView(PermissionRequiredMixin, CreateView):
    """
    Class-based view to create books with permission requirement.
    Uses can_create permission to control access.
    """
    model = Book
    fields = ['title', 'author', 'publication_year']
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create'

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class-based view to update books with permission requirement.
    Uses can_edit permission to control access.
    """
    model = Book
    fields = ['title', 'author', 'publication_year']
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_edit'

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Class-based view to delete books with permission requirement.
    Uses can_delete permission to control access.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'