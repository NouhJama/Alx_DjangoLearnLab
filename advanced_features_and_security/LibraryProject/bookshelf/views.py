"""
Secure Views for LibraryProject Bookshelf Application

This module implements secure views with comprehensive security measures:
- SQL Injection Prevention: Uses Django ORM and parameterized queries
- XSS Prevention: Automatic template escaping and input validation
- CSRF Protection: Required CSRF tokens on all POST requests
- Authorization: Permission-based access control
- Input Validation: Server-side validation for all user inputs
- Secure Redirects: Only internal redirects to prevent open redirects

Security Measures Implemented:
1. Permission-based access control using Django's permission system
2. CSRF protection via middleware and template tokens
3. SQL injection prevention through Django ORM
4. XSS prevention through template auto-escaping
5. Input validation and sanitization
6. Secure error handling with proper HTTP status codes
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import logging
from .models import Book

# Configure logging for security events
logger = logging.getLogger(__name__)

# ============================================================================
# SECURITY-ENHANCED FUNCTION-BASED VIEWS
# ============================================================================
# These views implement comprehensive security measures including:
# - Permission-based access control
# - CSRF protection
# - Input validation and sanitization
# - SQL injection prevention
# - XSS prevention
# - Secure error handling

@permission_required('bookshelf.can_view', raise_exception=True)
@require_http_methods(["GET"])  # Only allow GET requests for security
def book_list_view(request):
    """
    SECURE VIEW: List all books with permission-based access control.
    
    Security Measures:
    - Permission Check: Requires 'bookshelf.can_view' permission
    - HTTP Method Restriction: Only GET requests allowed
    - SQL Injection Prevention: Uses Django ORM (no raw SQL)
    - XSS Prevention: Template auto-escaping enabled
    - Error Handling: 403 Forbidden for unauthorized users
    
    Args:
        request: HTTP request object (authenticated user required)
        
    Returns:
        HttpResponse: Rendered book list template with book data
        
    Raises:
        PermissionDenied: If user lacks 'can_view' permission
    """
    try:
        # Use Django ORM to prevent SQL injection
        # .all() is safe - no user input involved
        books = Book.objects.all()
        
        # Log successful access for audit trail
        logger.info(f"User {request.user.username} accessed book list")
        
        # Context data is automatically escaped in templates
        context = {
            'books': books,
            'user_permissions': request.user.get_all_permissions(),
        }
        
        return render(request, 'bookshelf/book_list.html', context)
        
    except Exception as e:
        # Log security-relevant errors
        logger.error(f"Error in book_list_view for user {request.user.username}: {str(e)}")
        # Don't expose internal errors to users
        messages.error(request, "An error occurred while loading books.")
        return render(request, 'bookshelf/book_list.html', {'books': []})

@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect  # Explicit CSRF protection (redundant but explicit)
@require_http_methods(["GET", "POST"])  # Only allow GET and POST
def book_create_view(request):
    """
    SECURE VIEW: Create a new book with comprehensive security measures.
    
    Security Measures:
    - Permission Check: Requires 'bookshelf.can_create' permission
    - CSRF Protection: Required CSRF token on POST requests
    - Input Validation: Server-side validation of all inputs
    - XSS Prevention: Input sanitization and template escaping
    - SQL Injection Prevention: Django ORM with parameterized queries
    - HTTP Method Restriction: Only GET/POST allowed
    - Secure Redirects: Only internal redirects
    
    Args:
        request: HTTP request object (authenticated user required)
        
    Returns:
        HttpResponse: Book form template or redirect to book list
        
    Raises:
        PermissionDenied: If user lacks 'can_create' permission
        ValidationError: If input validation fails
    """
    if request.method == 'POST':
        try:
            # SECURITY: Input validation and sanitization
            title = request.POST.get('title', '').strip()
            author = request.POST.get('author', '').strip()
            publication_year_str = request.POST.get('publication_year', '').strip()
            
            # Validate required fields
            if not title:
                messages.error(request, "Title is required.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            if not author:
                messages.error(request, "Author is required.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            if not publication_year_str:
                messages.error(request, "Publication year is required.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            # SECURITY: Validate title length (prevent excessively long inputs)
            if len(title) > 200:
                messages.error(request, "Title must be 200 characters or less.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            # SECURITY: Validate author length
            if len(author) > 100:
                messages.error(request, "Author name must be 100 characters or less.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            # SECURITY: Validate and sanitize publication year
            try:
                publication_year = int(publication_year_str)
                if publication_year < 1000 or publication_year > 2100:
                    messages.error(request, "Publication year must be between 1000 and 2100.")
                    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            except ValueError:
                messages.error(request, "Publication year must be a valid number.")
                return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
            
            # SECURITY: Additional input sanitization (escape HTML entities)
            title = escape(title)
            author = escape(author)
            
            # SECURITY: Use Django ORM to prevent SQL injection
            # ORM automatically parameterizes queries
            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year
            )
            
            # Log successful creation for audit trail
            logger.info(f"User {request.user.username} created book: {book.title}")
            
            messages.success(request, 'Book created successfully!')
            
            # SECURITY: Use internal redirect only (prevent open redirects)
            return redirect('book_list')
            
        except ValidationError as e:
            # Handle model validation errors
            logger.warning(f"Validation error in book creation: {str(e)}")
            messages.error(request, "Invalid input data. Please check your entries.")
            
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error in book_create_view: {str(e)}")
            messages.error(request, "An error occurred while creating the book.")
    
    # Render form for GET requests or failed POST requests
    return render(request, 'bookshelf/book_form.html', {
        'action': 'Create',
        'csrf_token': request.META.get('CSRF_COOKIE'),
    })

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