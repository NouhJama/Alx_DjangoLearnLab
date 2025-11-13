# Django Permissions and Groups Setup Guide

## Overview
This Django application demonstrates custom permissions and role-based access control using Django's built-in auth system. The implementation uses custom permissions on the Book model with four distinct permission levels: `can_view`, `can_create`, `can_edit`, and `can_delete`.

## Custom Permissions Configuration

### Book Model Permissions
Located in `bookshelf/models.py`, the Book model defines custom permissions:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_create", "Can create a new book"),
            ("can_edit", "Can change an existing book"),
            ("can_delete", "Can delete a book"),
            ("can_view", "Can view book details"),
        ]
```

### Permission Levels Explained
- **`can_view`**: Allows users to see the book list and view book details
- **`can_create`**: Allows users to add new books to the library
- **`can_edit`**: Allows users to modify existing book information
- **`can_delete`**: Allows users to remove books from the library

## Groups and Roles

The system defines three user groups with different permission combinations:

### 1. Viewers Group
- **Permissions**: `can_view` only
- **Access Level**: Read-only access to book catalog
- **Use Case**: Regular library visitors, students

### 2. Editors Group  
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access Level**: Can view, add, and modify books (cannot delete)
- **Use Case**: Librarians, content managers

### 3. Managers Group
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access Level**: Full administrative access
- **Use Case**: Library administrators, system managers

## Implementation Details

### View-Level Permission Enforcement

#### Function-Based Views
```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list_view(request):
    # View implementation with permission check
```

#### Class-Based Views
```python
class BookListView(PermissionRequiredMixin, ListView):
    model = Book
    permission_required = 'bookshelf.can_view'
```

### Template-Level Permission Checks
Templates use Django's `perms` context variable to conditionally show/hide elements:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}" class="btn btn-create">Add New Book</a>
{% else %}
    <span style="color: #666;">Add New Book (No Permission)</span>
{% endif %}
```

## Setup and Testing

### Automated Setup
Run the management command to create test environment:

```bash
python manage.py setup_permissions_test
```

This command creates:
- Three user groups with appropriate permissions
- Three test users (one for each group)
- Sample book data for testing

### Test Users Created
| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| `viewer_user` | `testpass123` | Viewers | can_view |
| `editor_user` | `testpass123` | Editors | can_view, can_create, can_edit |
| `manager_user` | `testpass123` | Managers | can_view, can_create, can_edit, can_delete |

### Manual Testing Steps

1. **Start the Django server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the admin interface**: http://127.0.0.1:8000/admin/
   - Login with test users to verify group membership

3. **Test permission enforcement**: http://127.0.0.1:8000/bookshelf/books/
   - Login as different users
   - Observe how UI elements change based on permissions
   - Try accessing restricted functions

4. **Test scenarios**:
   - **As viewer_user**: Can only see book list, no action buttons
   - **As editor_user**: Can see list, create, and edit buttons (no delete)
   - **As manager_user**: Can see all buttons and perform all actions

### URL Structure
```
/bookshelf/books/                    # Book list (requires can_view)
/bookshelf/books/create/             # Create book (requires can_create)
/bookshelf/books/<id>/edit/          # Edit book (requires can_edit)
/bookshelf/books/<id>/delete/        # Delete book (requires can_delete)
```

## Security Features

### Permission Enforcement
- **View Level**: `@permission_required` decorator and `PermissionRequiredMixin`
- **Template Level**: Conditional rendering based on user permissions
- **URL Level**: Django's built-in permission system integration

### Error Handling
- Users without required permissions receive 403 Forbidden responses
- Graceful degradation in templates (buttons become disabled/hidden)
- Clear permission requirement indicators in UI

## Best Practices Implemented

1. **Principle of Least Privilege**: Users get only necessary permissions
2. **Defense in Depth**: Multiple layers of permission checks
3. **User Experience**: Clear indication of permission requirements
4. **Separation of Concerns**: Permissions defined at model level
5. **Testability**: Automated setup for consistent testing environment

## Extending the System

### Adding New Permissions
1. Add permission to model's Meta class
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update groups with new permissions
4. Add permission checks to relevant views and templates

### Creating New Groups
```python
from django.contrib.auth.models import Group, Permission

# Create group
group = Group.objects.create(name='CustomGroup')

# Add permissions
permissions = Permission.objects.filter(codename__in=['can_view', 'can_create'])
group.permissions.set(permissions)
```

### Assigning Users to Groups
```python
from django.contrib.auth.models import Group
from bookshelf.models import CustomUser

user = CustomUser.objects.get(username='username')
group = Group.objects.get(name='GroupName')
user.groups.add(group)
```

## Troubleshooting

### Common Issues
1. **Permission not found**: Ensure migrations are applied after adding custom permissions
2. **Template permissions not working**: Verify user is authenticated and has correct group membership
3. **403 Errors**: Check that user has required permission and `raise_exception=True` is set

### Debugging Tips
- Use Django admin to verify user group memberships
- Check `request.user.get_all_permissions()` in views
- Use `{% debug %}` in templates to inspect permission context

This implementation provides a robust, scalable foundation for role-based access control in Django applications.