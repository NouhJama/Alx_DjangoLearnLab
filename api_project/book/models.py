from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    """
    A simple Book model with basic information
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    author = models.CharField(max_length=100, help_text="The author's name")
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True, help_text="13-digit ISBN number")
    published_date = models.DateField(help_text="The date when the book was published")
    pages = models.PositiveIntegerField(default=0, help_text="Number of pages in the book")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price of the book")
    description = models.TextField(blank=True, help_text="A brief description of the book")
    is_available = models.BooleanField(default=True, help_text="Whether the book is available for purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_recent(self):
        """Check if the book was published in the last 5 years"""
        from datetime import date, timedelta
        five_years_ago = date.today() - timedelta(days=365*5)
        return self.published_date >= five_years_ago
