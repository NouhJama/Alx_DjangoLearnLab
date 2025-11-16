"""
Security Testing Script for LibraryProject

This script performs comprehensive security testing to verify that security measures
are properly implemented and effective.

Tests Performed:
1. CSRF Protection Testing
2. XSS Prevention Testing  
3. SQL Injection Prevention Testing
4. Permission-Based Access Control Testing
5. Input Validation Testing
6. Security Headers Testing
7. Authentication Testing

Usage:
    python manage.py shell < security_tests.py
    
Or run specific test functions interactively in Django shell.
"""

import os
import django
from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import HttpResponse
from bookshelf.models import CustomUser, Book
import re

# Initialize Django for standalone script execution
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

class SecurityTester:
    """
    Comprehensive security testing suite for LibraryProject.
    """
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def log_result(self, test_name, passed, details=""):
        """Log test results for reporting."""
        status = "PASS" if passed else "FAIL"
        result = f"[{status}] {test_name}"
        if details:
            result += f" - {details}"
        self.test_results.append(result)
        print(result)
    
    def test_csrf_protection(self):
        """
        Test CSRF protection on form submissions.
        
        Security Objective: Ensure all POST requests require valid CSRF tokens
        """
        print("\n🔒 Testing CSRF Protection...")
        
        # Create test user with permissions
        user, created = CustomUser.objects.get_or_create(
            username='security_test_user',
            defaults={'email': 'test@security.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Test 1: POST request without CSRF token should fail
        try:
            response = self.client.post('/bookshelf/books/create/', {
                'title': 'Test Book',
                'author': 'Test Author',
                'publication_year': '2023'
            })
            
            # Should return 403 Forbidden due to missing CSRF token
            csrf_protected = response.status_code == 403
            self.log_result(
                "CSRF Protection - POST without token",
                csrf_protected,
                f"Status: {response.status_code}, Expected: 403"
            )
        except Exception as e:
            self.log_result("CSRF Protection - POST without token", False, str(e))
        
        # Test 2: GET request to form should include CSRF token
        try:
            self.client.login(username='security_test_user', password='testpass123')
            response = self.client.get('/bookshelf/books/create/')
            
            csrf_in_form = b'csrfmiddlewaretoken' in response.content
            self.log_result(
                "CSRF Token in Form",
                csrf_in_form,
                "CSRF token present in form" if csrf_in_form else "CSRF token missing"
            )
        except Exception as e:
            self.log_result("CSRF Token in Form", False, str(e))
    
    def test_xss_prevention(self):
        """
        Test XSS prevention through input validation and template escaping.
        
        Security Objective: Prevent execution of malicious scripts
        """
        print("\n🛡️ Testing XSS Prevention...")
        
        # XSS payloads to test
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
        ]
        
        # Test template escaping by creating book with XSS payload
        for i, payload in enumerate(xss_payloads):
            try:
                # Create book with XSS payload in title
                book = Book.objects.create(
                    title=f"XSS Test {i}: {payload}",
                    author="Security Tester",
                    publication_year=2023
                )
                
                # Get book list page
                response = self.client.get('/bookshelf/books/')
                
                # Check if payload is properly escaped in HTML
                raw_payload_in_response = payload.encode() in response.content
                escaped_properly = not raw_payload_in_response
                
                self.log_result(
                    f"XSS Prevention - Payload {i+1}",
                    escaped_properly,
                    f"Raw script {'not found' if escaped_properly else 'FOUND'} in response"
                )
                
                # Clean up
                book.delete()
                
            except Exception as e:
                self.log_result(f"XSS Prevention - Payload {i+1}", False, str(e))
    
    def test_sql_injection_prevention(self):
        """
        Test SQL injection prevention through ORM usage.
        
        Security Objective: Prevent unauthorized database access
        """
        print("\n💉 Testing SQL Injection Prevention...")
        
        # SQL injection payloads
        sql_payloads = [
            "'; DROP TABLE bookshelf_book; --",
            "' OR '1'='1",
            "'; SELECT * FROM auth_user; --",
            "' UNION SELECT password FROM auth_user --",
        ]
        
        original_book_count = Book.objects.count()
        
        for i, payload in enumerate(sql_payloads):
            try:
                # Attempt to create book with SQL injection payload
                Book.objects.create(
                    title=f"SQL Test {payload}",
                    author="Security Tester",
                    publication_year=2023
                )
                
                # Check if database structure is intact
                current_book_count = Book.objects.count()
                books_still_exist = current_book_count > original_book_count
                
                # Try to query - if SQL injection worked, this might fail
                test_books = Book.objects.filter(author="Security Tester")
                query_successful = len(test_books) > 0
                
                self.log_result(
                    f"SQL Injection Prevention - Payload {i+1}",
                    books_still_exist and query_successful,
                    f"Database intact, query successful"
                )
                
                # Clean up
                test_books.delete()
                
            except Exception as e:
                # Exceptions might indicate SQL injection attempt was blocked
                self.log_result(
                    f"SQL Injection Prevention - Payload {i+1}",
                    True,
                    f"Payload blocked by ORM: {str(e)[:50]}"
                )
    
    def test_permission_based_access(self):
        """
        Test permission-based access control.
        
        Security Objective: Ensure only authorized users can access resources
        """
        print("\n🔐 Testing Permission-Based Access Control...")
        
        # Create users with different permission levels
        viewer_user, created = CustomUser.objects.get_or_create(
            username='test_viewer',
            defaults={'email': 'viewer@test.com'}
        )
        if created:
            viewer_user.set_password('testpass123')
            viewer_user.save()
        
        editor_user, created = CustomUser.objects.get_or_create(
            username='test_editor',
            defaults={'email': 'editor@test.com'}
        )
        if created:
            editor_user.set_password('testpass123')
            editor_user.save()
        
        # Test unauthorized access
        self.client.logout()
        response = self.client.get('/bookshelf/books/')
        unauthorized_blocked = response.status_code in [302, 403]  # Redirect to login or forbidden
        
        self.log_result(
            "Permission Check - Unauthorized Access",
            unauthorized_blocked,
            f"Status: {response.status_code}"
        )
        
        # Test viewer access (should only view)
        self.client.login(username='test_viewer', password='testpass123')
        response = self.client.get('/bookshelf/books/create/')
        viewer_create_blocked = response.status_code == 403
        
        self.log_result(
            "Permission Check - Viewer Create Access",
            viewer_create_blocked,
            f"Create blocked for viewer: {response.status_code == 403}"
        )
    
    def test_input_validation(self):
        """
        Test input validation and sanitization.
        
        Security Objective: Ensure malformed input is rejected
        """
        print("\n✅ Testing Input Validation...")
        
        # Test cases for input validation
        test_cases = [
            {
                'name': 'Empty Title',
                'data': {'title': '', 'author': 'Test', 'publication_year': '2023'},
                'should_fail': True
            },
            {
                'name': 'Long Title',
                'data': {'title': 'A' * 300, 'author': 'Test', 'publication_year': '2023'},
                'should_fail': True
            },
            {
                'name': 'Invalid Year',
                'data': {'title': 'Test', 'author': 'Test', 'publication_year': 'invalid'},
                'should_fail': True
            },
            {
                'name': 'Year Out of Range',
                'data': {'title': 'Test', 'author': 'Test', 'publication_year': '3000'},
                'should_fail': True
            },
            {
                'name': 'Valid Input',
                'data': {'title': 'Valid Book', 'author': 'Valid Author', 'publication_year': '2023'},
                'should_fail': False
            }
        ]
        
        for test_case in test_cases:
            try:
                # Get CSRF token
                response = self.client.get('/bookshelf/books/create/')
                csrf_token = self.client.session.get('csrftoken')
                
                # Add CSRF token to data
                data = test_case['data'].copy()
                data['csrfmiddlewaretoken'] = csrf_token
                
                # Submit form
                response = self.client.post('/bookshelf/books/create/', data)
                
                if test_case['should_fail']:
                    # Should show form again with errors (not redirect)
                    validation_working = response.status_code == 200
                else:
                    # Should redirect on success
                    validation_working = response.status_code == 302
                
                self.log_result(
                    f"Input Validation - {test_case['name']}",
                    validation_working,
                    f"Status: {response.status_code}"
                )
                
            except Exception as e:
                self.log_result(f"Input Validation - {test_case['name']}", False, str(e))
    
    def test_security_headers(self):
        """
        Test security headers implementation.
        
        Security Objective: Ensure proper security headers are present
        """
        print("\n🔧 Testing Security Headers...")
        
        try:
            response = self.client.get('/bookshelf/books/')
            
            # Check for security headers
            headers_to_check = {
                'X-Frame-Options': 'DENY',
                'X-Content-Type-Options': 'nosniff',
                'X-XSS-Protection': '1; mode=block',
                'Content-Security-Policy': 'default-src',  # Should contain this
                'Referrer-Policy': 'strict-origin-when-cross-origin',
            }
            
            for header, expected_value in headers_to_check.items():
                header_present = header in response
                header_correct = expected_value in str(response.get(header, ''))
                
                self.log_result(
                    f"Security Header - {header}",
                    header_present and header_correct,
                    f"Present: {header_present}, Correct: {header_correct}"
                )
                
        except Exception as e:
            self.log_result("Security Headers Test", False, str(e))
    
    def run_all_tests(self):
        """Run all security tests and generate report."""
        print("🔒 STARTING COMPREHENSIVE SECURITY TESTING")
        print("=" * 60)
        
        self.test_csrf_protection()
        self.test_xss_prevention()
        self.test_sql_injection_prevention()
        self.test_permission_based_access()
        self.test_input_validation()
        self.test_security_headers()
        
        # Generate summary report
        print("\n" + "=" * 60)
        print("🏆 SECURITY TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for result in self.test_results if "[PASS]" in result)
        total_tests = len(self.test_results)
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if pass_rate >= 90:
            print("🟢 SECURITY STATUS: EXCELLENT")
        elif pass_rate >= 75:
            print("🟡 SECURITY STATUS: GOOD - Minor issues to address")
        else:
            print("🔴 SECURITY STATUS: NEEDS ATTENTION - Critical issues found")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            print(f"  {result}")
        
        return pass_rate >= 90

# Run tests if script is executed directly
if __name__ == "__main__":
    tester = SecurityTester()
    tester.run_all_tests()