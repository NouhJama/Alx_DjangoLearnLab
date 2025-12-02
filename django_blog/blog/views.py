from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class UserRegistrationForm(UserCreationForm):
    # Additional fields for user registration
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        # create user object without saving first
        user = super().save(commit=False)
        # set additional fields to be saved to the db table.
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        # save the user object to the db table
        if commit: # if commit is True
            user.save() # save the user object to the db table
        return user
    
def register_view(request):
    """
    View to handle user registration.
    - GET: Display registration form.
    - POST: Process registration form.
    """
    if request.method == "POST": # if the request method is POST
        # Just put the submitted data by the user to the form
        form = UserRegistrationForm(request.POST) 
        if form.is_valid(): # if the form data passed all validations
            form.save() # save the user to the db table
            return render(request, "registration/success.html")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})
