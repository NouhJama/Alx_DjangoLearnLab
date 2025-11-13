"""
Django management command to set up permission testing environment.

This command creates test users and groups with different permission levels
to demonstrate and test the custom permissions system.

Usage: python manage.py setup_permissions_test

Groups Created:
- Editors: can_create, can_edit, can_view permissions
- Viewers: can_view permission only  
- Managers: all permissions (can_create, can_edit, can_delete, can_view)

Test Users Created:
- viewer_user (password: testpass123) - member of Viewers group
- editor_user (password: testpass123) - member of Editors group  
- manager_user (password: testpass123) - member of Managers group
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import CustomUser, Book


class Command(BaseCommand):
    help = 'Set up permissions testing environment with users and groups'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up permissions testing environment...'))
        
        # Get the Book content type for permissions
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all custom permissions for Book model
        permissions = Permission.objects.filter(content_type=book_content_type)
        
        # Create permission mapping
        permission_map = {}
        for perm in permissions:
            permission_map[perm.codename] = perm
            self.stdout.write(f'  📋 Found permission: {perm.name} ({perm.codename})')
        
        # Create Groups with different permission levels
        groups_config = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'], 
            'Managers': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }
        
        created_groups = {}
        for group_name, permission_codes in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'  ✅ Created group: {group_name}')
            else:
                self.stdout.write(f'  📌 Group already exists: {group_name}')
            
            # Clear existing permissions and add new ones
            group.permissions.clear()
            for code in permission_codes:
                if code in permission_map:
                    group.permissions.add(permission_map[code])
                    self.stdout.write(f'    ➕ Added {code} permission to {group_name}')
            
            created_groups[group_name] = group
        
        # Create test users
        test_users = [
            {
                'username': 'viewer_user',
                'password': 'testpass123',
                'email': 'viewer@library.com',
                'first_name': 'View',
                'last_name': 'User',
                'group': 'Viewers'
            },
            {
                'username': 'editor_user', 
                'password': 'testpass123',
                'email': 'editor@library.com',
                'first_name': 'Editor',
                'last_name': 'User',
                'group': 'Editors'
            },
            {
                'username': 'manager_user',
                'password': 'testpass123', 
                'email': 'manager@library.com',
                'first_name': 'Manager',
                'last_name': 'User',
                'group': 'Managers'
            }
        ]
        
        for user_data in test_users:
            username = user_data['username']
            group_name = user_data['group']
            password = user_data['password']
            
            # Create or get user
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'], 
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  👤 Created user: {username}')
            else:
                self.stdout.write(f'  📌 User already exists: {username}')
            
            # Add user to group
            group = created_groups[group_name]
            user.groups.clear()  # Remove from all groups first
            user.groups.add(group)
            self.stdout.write(f'    🔗 Added {username} to {group_name} group')
        
        # Create some sample books for testing
        sample_books = [
            {'title': 'Django for Beginners', 'author': 'William Vincent', 'publication_year': 2022},
            {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'publication_year': 2019},
            {'title': 'Clean Code', 'author': 'Robert Martin', 'publication_year': 2008},
        ]
        
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'  📚 Created sample book: {book.title}')
        
        # Display testing instructions
        self.stdout.write(self.style.SUCCESS('\n🎯 Permission Testing Setup Complete!'))
        self.stdout.write('\n📖 Testing Instructions:')
        self.stdout.write('=' * 50)
        
        for user_data in test_users:
            username = user_data['username'] 
            group = user_data['group']
            self.stdout.write(f'\n🔐 Login as: {username}')
            self.stdout.write(f'   Password: testpass123') 
            self.stdout.write(f'   Group: {group}')
            
            # Show what permissions this user should have
            group_perms = groups_config[group]
            self.stdout.write(f'   Permissions: {", ".join(group_perms)}')
            
            # Show what they should be able to do
            if 'can_view' in group_perms:
                self.stdout.write('   ✅ Can view book list')
            if 'can_create' in group_perms:
                self.stdout.write('   ✅ Can create new books')
            if 'can_edit' in group_perms:
                self.stdout.write('   ✅ Can edit existing books')  
            if 'can_delete' in group_perms:
                self.stdout.write('   ✅ Can delete books')
        
        self.stdout.write('\n🌐 Test URLs:')
        self.stdout.write('  Book List: http://127.0.0.1:8000/bookshelf/books/')
        self.stdout.write('  Admin: http://127.0.0.1:8000/admin/')
        
        self.stdout.write('\n🧪 How to Test:')
        self.stdout.write('1. Login as different users at /admin/')
        self.stdout.write('2. Visit /bookshelf/books/ to test permissions')
        self.stdout.write('3. Try accessing create/edit/delete functions')
        self.stdout.write('4. Notice how UI elements change based on permissions')
        
        self.stdout.write(self.style.SUCCESS('\n✨ Happy testing!'))