from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_create", "Can create a new book"),
            ("can_edit", "Can change an existing book"),
            ("can_delete", "Can delete a book"),
            ("can_view", "Can view book details"),
        ]

