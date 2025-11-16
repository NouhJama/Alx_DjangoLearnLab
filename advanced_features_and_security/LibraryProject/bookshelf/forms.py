"""
Django Forms for LibraryProject Bookshelf Application

This module implements secure Django forms with comprehensive validation,
CSRF protection, and XSS prevention measures. All forms follow Django
security best practices and include detailed validation logic.

Security Features Implemented:
- Input validation and sanitization
- Field-level security constraints
- Custom validators for security
- HTML escaping and XSS prevention
- Form-level validation with detailed error messages
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.html import escape, strip_tags
from django.core.exceptions import ValidationError
import re
from .models import Book, CustomUser


class BookForm(forms.ModelForm):
    """
    Secure Book creation and editing form with comprehensive validation.
    
    Security Features:
    - Input sanitization and validation
    - Length constraints to prevent buffer overflow
    - Pattern validation to prevent injection attacks
    - HTML escaping to prevent XSS
    - Custom clean methods for additional security
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # SECURITY: Define field constraints and validation
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title (max 200 characters)',
                'maxlength': '200',  # HTML5 client-side validation
                'required': True,
                'pattern': r'^[^<>]*$',  # No angle brackets (XSS prevention)
                'aria-describedby': 'title-help',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name (max 100 characters)',
                'maxlength': '100',  # HTML5 client-side validation
                'required': True,
                'pattern': r'^[^<>]*$',  # No angle brackets (XSS prevention)
                'aria-describedby': 'author-help',
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year (1000-2100)',
                'min': '1000',  # HTML5 client-side validation
                'max': '2100',  # HTML5 client-side validation
                'required': True,
                'aria-describedby': 'year-help',
            }),
        }
        
        # SECURITY: Custom labels with security notices
        labels = {
            'title': 'Book Title *',
            'author': 'Author Name *',
            'publication_year': 'Publication Year *',
        }
        
        # SECURITY: Help text for users
        help_texts = {
            'title': 'Required field, maximum 200 characters. No HTML tags allowed.',
            'author': 'Required field, maximum 100 characters. No HTML tags allowed.',
            'publication_year': 'Required field, must be between 1000 and 2100.',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with additional security measures.
        
        SECURITY: Set up validators and security attributes during initialization
        """
        super().__init__(*args, **kwargs)
        
        # SECURITY: Add server-side validators for each field
        self.fields['title'].validators.extend([
            RegexValidator(
                regex=r'^[^<>]*$',
                message='Title cannot contain HTML tags or angle brackets for security reasons.',
                code='invalid_characters'
            ),
        ])
        
        self.fields['author'].validators.extend([
            RegexValidator(
                regex=r'^[^<>]*$',
                message='Author name cannot contain HTML tags or angle brackets for security reasons.',
                code='invalid_characters'
            ),
        ])
        
        self.fields['publication_year'].validators.extend([
            MinValueValidator(
                1000,
                message='Publication year must be 1000 or later.'
            ),
            MaxValueValidator(
                2100,
                message='Publication year must be 2100 or earlier.'
            ),
        ])
        
        # SECURITY: Set all fields as required
        for field_name, field in self.fields.items():
            field.required = True
            # Add CSS classes for styling and JavaScript validation
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        """
        Custom validation for title field with security measures.
        
        SECURITY: Sanitize input, validate length, and prevent malicious content
        """
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError('Title is required.')
        
        # SECURITY: Strip and sanitize input
        title = title.strip()
        title = escape(title)  # HTML escape for XSS prevention
        
        # SECURITY: Length validation
        if len(title) > 200:
            raise ValidationError('Title must be 200 characters or less.')
        
        if len(title) < 1:
            raise ValidationError('Title cannot be empty.')
        
        # SECURITY: Content validation - prevent potentially dangerous content
        if '<' in title or '>' in title:
            raise ValidationError('Title cannot contain HTML tags for security reasons.')
        
        # SECURITY: Check for SQL injection patterns (defense in depth)
        dangerous_patterns = [
            r'(?i)(union\s+select)',
            r'(?i)(drop\s+table)',
            r'(?i)(delete\s+from)',
            r'(?i)(insert\s+into)',
            r'(?i)(update\s+.*\s+set)',
            r'(--|/\*|\*/)',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, title):
                raise ValidationError('Title contains potentially dangerous content.')
        
        return title

    def clean_author(self):
        """
        Custom validation for author field with security measures.
        
        SECURITY: Sanitize input, validate length, and prevent malicious content
        """
        author = self.cleaned_data.get('author')
        
        if not author:
            raise ValidationError('Author is required.')
        
        # SECURITY: Strip and sanitize input
        author = author.strip()
        author = escape(author)  # HTML escape for XSS prevention
        
        # SECURITY: Length validation
        if len(author) > 100:
            raise ValidationError('Author name must be 100 characters or less.')
        
        if len(author) < 1:
            raise ValidationError('Author name cannot be empty.')
        
        # SECURITY: Content validation - prevent potentially dangerous content
        if '<' in author or '>' in author:
            raise ValidationError('Author name cannot contain HTML tags for security reasons.')
        
        # SECURITY: Check for SQL injection patterns (defense in depth)
        dangerous_patterns = [
            r'(?i)(union\s+select)',
            r'(?i)(drop\s+table)',
            r'(?i)(delete\s+from)',
            r'(?i)(insert\s+into)',
            r'(?i)(update\s+.*\s+set)',
            r'(--|/\*|\*/)',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, author):
                raise ValidationError('Author name contains potentially dangerous content.')
        
        return author

    def clean_publication_year(self):
        """
        Custom validation for publication year with security measures.
        
        SECURITY: Validate numeric input and reasonable ranges
        """
        year = self.cleaned_data.get('publication_year')
        
        if year is None:
            raise ValidationError('Publication year is required.')
        
        # SECURITY: Type validation
        if not isinstance(year, int):
            try:
                year = int(year)
            except (ValueError, TypeError):
                raise ValidationError('Publication year must be a valid number.')
        
        # SECURITY: Range validation
        if year < 1000:
            raise ValidationError('Publication year must be 1000 or later.')
        
        if year > 2100:
            raise ValidationError('Publication year must be 2100 or earlier.')
        
        return year

    def clean(self):
        """
        Form-level validation with additional security checks.
        
        SECURITY: Cross-field validation and comprehensive security verification
        """
        cleaned_data = super().clean()
        
        # SECURITY: Ensure all required fields are present
        required_fields = ['title', 'author', 'publication_year']
        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, f'{field_name.replace("_", " ").title()} is required.')
        
        # SECURITY: Additional cross-field validation
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        
        if title and author:
            # SECURITY: Prevent duplicate content (basic check)
            if title.lower() == author.lower():
                raise ValidationError('Title and author cannot be identical.')
        
        return cleaned_data

    def save(self, commit=True):
        """
        Secure save method with additional validation.
        
        SECURITY: Final validation before database save
        """
        instance = super().save(commit=False)
        
        # SECURITY: Final sanitization before save
        if hasattr(instance, 'title'):
            instance.title = escape(instance.title.strip())
        
        if hasattr(instance, 'author'):
            instance.author = escape(instance.author.strip())
        
        if commit:
            instance.save()
        
        return instance


class CustomUserCreationForm(UserCreationForm):
    """
    Secure user registration form with enhanced validation.
    
    Security Features:
    - Strong password requirements
    - Email validation and sanitization
    - Profile field validation
    - Custom security measures
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'maxlength': '254',  # RFC 5321 email length limit
        }),
        help_text='Required. Enter a valid email address.'
    )
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': '2010-01-01',  # Minimum age requirement
            'min': '1900-01-01',  # Reasonable date range
        }),
        help_text='Optional. Your date of birth (you must be at least 15 years old).'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize form with security enhancements.
        """
        super().__init__(*args, **kwargs)
        
        # SECURITY: Add custom attributes to username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'maxlength': '150',  # Django default max length
            'pattern': r'^[a-zA-Z0-9@/./+/-/_]*$',  # Django username pattern
        })
        
        # SECURITY: Enhance password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter a strong password',
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })

    def clean_email(self):
        """
        Custom email validation with security measures.
        """
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError('Email is required.')
        
        # SECURITY: Sanitize email
        email = email.strip().lower()
        
        # SECURITY: Additional email validation
        if len(email) > 254:  # RFC 5321 limit
            raise ValidationError('Email address is too long.')
        
        # SECURITY: Check for existing email
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        
        return email

    def clean_date_of_birth(self):
        """
        Custom date of birth validation.
        """
        dob = self.cleaned_data.get('date_of_birth')
        
        if dob:
            from datetime import date
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            # SECURITY: Age validation for compliance
            if age < 15:
                raise ValidationError('You must be at least 15 years old to register.')
            
            if age > 120:
                raise ValidationError('Please enter a valid date of birth.')
        
        return dob

    def save(self, commit=True):
        """
        Secure save method for user creation.
        """
        user = super().save(commit=False)
        
        # SECURITY: Set email field
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Secure user profile change form.
    """
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo')

    def __init__(self, *args, **kwargs):
        """
        Initialize form with security measures.
        """
        super().__init__(*args, **kwargs)
        
        # SECURITY: Remove password field from change form
        if 'password' in self.fields:
            del self.fields['password']
        
        # SECURITY: Add security attributes
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = 'form-control'


class BookSearchForm(forms.Form):
    """
    Secure search form for books with input validation.
    
    Security Features:
    - Input sanitization
    - Length limits
    - XSS prevention
    """
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title or author...',
            'maxlength': '200',
        }),
        help_text='Enter search terms (maximum 200 characters)'
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All Fields'),
            ('title', 'Title Only'),
            ('author', 'Author Only'),
        ],
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    def clean_query(self):
        """
        Custom validation for search query with security measures.
        """
        query = self.cleaned_data.get('query', '')
        
        if query:
            # SECURITY: Sanitize search input
            query = query.strip()
            query = escape(query)  # Prevent XSS
            
            # SECURITY: Length validation
            if len(query) > 200:
                raise ValidationError('Search query must be 200 characters or less.')
            
            # SECURITY: Prevent potentially dangerous search patterns
            dangerous_patterns = [
                r'(?i)(union\s+select)',
                r'(?i)(drop\s+table)',
                r'(?i)(delete\s+from)',
                r'(--|/\*|\*/)',
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, query):
                    raise ValidationError('Search query contains invalid characters.')
        
        return query