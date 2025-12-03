from django.shortcuts import render, redirect
from django.contrib.auth import login

from blog.forms import ProfileUpdateForm
from .models import Post, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    if request.method == "POST": # If the request method is POST
        form = RegisterForm(request.POST) # Instantiate the registration form with POST data
        if form.is_valid(): # If the form is valid
            user = form.save() # Save the new user
            login(request, user)    # Log the user in
            return redirect("blog-home") # Redirect to home page after successful registration
    else: # If the request method is GET    
        form = RegisterForm() # Instantiate an empty registration form
    # Render the registration template with the form    
    return render(request, "blog/registration.html", {"form": form})

class PostListView(generic.ListView):
    model = Post
    template_name = "blog/home.html"  # Specify your template name
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 5

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # Specify your template name   

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"  # Specify your template name

    def form_valid(self, form):
        # Set the author of the post to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"  # Specify your template name

    def form_valid(self, form):
        # Ensure the author of the post is the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"  # Specify your template name
    success_url = reverse_lazy("blog-home")

    def get_queryset(self):
        # Limit deletion to posts authored by the current user
        return super().get_queryset().filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post has been deleted successfully.")
        return super().delete(request, *args, **kwargs) 