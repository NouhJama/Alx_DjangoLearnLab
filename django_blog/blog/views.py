from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .models import Post, UserProfile, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterForm, PostForm, UserProfileForm, UpdatePostForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class LoginView(LoginView):  # ✅ CBV for login
    template_name = 'blog/login.html'


    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)
    
class LogoutView(LogoutView):  # ✅ CBV for logout
    template_name = 'blog/logout.html'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(generic.FormView):  # ✅ CBV for registration
    template_name = 'blog/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Save the user
        user = form.save()
        
        # Log the user in automatically
        LoginView(self.request, user)
        
        # Add success message
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}!')
        
        return super().form_valid(form)
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserCreationForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'blog/profile.html', context)



class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"  # Specify your template name
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.count()
        return context

class TaggedPostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Post.objects.filter(tags__name=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        context['total_posts'] = self.get_queryset().count()
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # Specify your template name   

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"  # Specify your template name

    def form_valid(self, form):
        # Set the author of the post to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"  # Specify your template name

    def form_valid(self, form):
        # Ensure the author of the post is the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Only allow the author to edit the post
        post = self.get_object()
        return self.request.user == post.author
    
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
    

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_id']})
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
def SearchPostView(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    
    context = {
        'posts': results,
        'total_posts': results.count(),
        'search_query': query
    }
    
    return render(request, 'blog/post_list.html', context)