from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Post, UserProfile
from django.contrib.auth.models import User
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