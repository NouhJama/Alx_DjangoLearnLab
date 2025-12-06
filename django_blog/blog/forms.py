from django import forms
from taggit.forms import TagWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment

# Form for user registration
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        # Include email, first_name, and last_name fields
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    """
    Override the save method to save additional fields.
    -GET: get the user instance without committing to the database.
    -Set the email, first_name, and last_name fields from cleaned_data. 
    -If commit is True, save the user instance to the database.
    -Return the user instance.
    """    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
    
# Form for user profile
class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ["bio", "location", "birth_date", "profile_picture"]

    def cleaned_email(self):
        return self.cleaned_data["email"]   
        # Exclude current user's email from uniqueness check
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
# Form for creating and updating blog posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post Title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post content here...'}),
            'tags': TagWidget(
                attrs={'placeholder': 'Add tags separated by commas', 'class': 'tag-input', 'data-role': 'tagsinput'}),
        }


    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content cannot be empty.")
        if len(content) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.") 
        return content
    
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post Title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post content here...'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title        
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return content