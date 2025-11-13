"""
Django shell script to test and verify permissions setup.
"""

from django.contrib.auth.models import Group, Permission
from bookshelf.models import CustomUser, Book
from django.contrib.contenttypes.models import ContentType

print("Permission System Verification")
print("=" * 50)

# Test users and their permissions
test_users = ['viewer_user', 'editor_user', 'manager_user']

for username in test_users:
    try:
        user = CustomUser.objects.get(username=username)
        print(f"\nUser: {user.username} ({user.first_name} {user.last_name})")
        
        # Get user groups
        groups = user.groups.all()
        print(f"   Groups: {', '.join([g.name for g in groups])}")
        
        # Get user permissions
        user_perms = user.get_all_permissions()
        book_perms = [p for p in user_perms if 'bookshelf' in p]
        print(f"   Book Permissions: {book_perms}")
        
        # Test specific permission checks
        perms_to_check = ['bookshelf.can_view', 'bookshelf.can_create', 
                         'bookshelf.can_edit', 'bookshelf.can_delete']
        
        print("   Permission Status:")
        for perm in perms_to_check:
            has_perm = user.has_perm(perm)
            status = "YES" if has_perm else "NO"
            perm_name = perm.split('.')[-1]
            print(f"     {status} {perm_name}")
            
    except CustomUser.DoesNotExist:
        print(f"ERROR: User {username} not found!")

# Verify groups and their permissions
print(f"\nGroups and Permissions Summary")
print("=" * 50)

groups = Group.objects.all()
for group in groups:
    print(f"\nGroup: {group.name}")
    perms = group.permissions.filter(content_type__app_label='bookshelf')
    perm_names = [p.codename for p in perms]
    print(f"   Permissions: {perm_names}")
    
    # Count users in group
    user_count = group.user_set.count()
    users = [u.username for u in group.user_set.all()]
    print(f"   Users ({user_count}): {users}")

# Verify sample books exist
print(f"\nSample Books")
print("=" * 30)
books = Book.objects.all()
for book in books:
    print(f"   {book.title} by {book.author} ({book.publication_year})")

print(f"\nTotal Books: {books.count()}")
print("Permission system verification complete!")