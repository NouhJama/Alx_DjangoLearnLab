from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Library, Book, Author, Librarian
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.
# Acces Control based on UserProfile role can be implemented here
@user_passes_test(lambda u: u.is_authenticated)

@user_passes_test(lambda u: u.is_authenticated) 
# Function-based view.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ListView for Books - displays all books
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/book_list.html'
    context_object_name = 'books'

# Function-based Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role-based views for the users
# You can expand this section based on your requirements for different roles
class admin_view(View):
    def get(self, request):
        # Logic for admin view
        return render(request, 'relationship_app/admin_view.html')

class librarian_view(View):
    def get(self, request):
        # Logic for librarian view
        return render(request, 'relationship_app/librarian_view.html')

class member_view(View):
    def get(self, request):
        # Logic for member view
        return render(request, 'relationship_app/member_view.html')
    
# view to add a new book
class add_book_view(PermissionRequiredMixin, View):
    permission_required = 'relationship_app.can_add_book'
    
    def get(self, request):
        # Logic to display add book form
        return render(request, 'relationship_app/add_book.html')
    
    def post(self, request):
        # Logic to handle book addition
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = Author.objects.get(id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('book-list')
    
# view to delete a book
class delete_book_view(PermissionRequiredMixin, View):
    permission_required = 'relationship_app.can_delete_book'
    
    def post(self, request, book_id):
        # Logic to handle book deletion
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect('book-list')
    
# view to change a book
class change_book_view(PermissionRequiredMixin, View):
    permission_required = 'relationship_app.can_change_book'
    
    def get(self, request, book_id):
        # Logic to display change book form
        book = Book.objects.get(id=book_id)
        return render(request, 'relationship_app/change_book.html', {'book': book})
    
    def post(self, request, book_id):
        # Logic to handle book change
        book = Book.objects.get(id=book_id)
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = Author.objects.get(id=author_id)
        book.save()
        return redirect('book-list')