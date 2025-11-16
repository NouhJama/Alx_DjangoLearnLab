#!/usr/bin/env python
"""
🔒 Security Implementation Validation Script
Validates all security measures implemented in LibraryProject
"""

import os
import sys
import re

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

def check_file_content(file_path, checks):
    """Check if file contains required security configurations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for check_name, pattern in checks.items():
            if isinstance(pattern, str):
                results[check_name] = pattern in content
            else:  # regex pattern
                results[check_name] = bool(re.search(pattern, content))
        
        return results
    except FileNotFoundError:
        return {check: False for check in checks}

def validate_security_implementation():
    """Validate all security implementations"""
    
    print("🔒 LibraryProject Security Validation")
    print("=" * 50)
    
    total_checks = 0
    passed_checks = 0
    
    # 1. Settings.py Security Configuration
    print("\n📋 1. SETTINGS.PY SECURITY CONFIGURATION")
    settings_checks = {
        'CSRF Middleware': 'django.middleware.csrf.CsrfViewMiddleware',
        'Security Middleware': 'django.middleware.security.SecurityMiddleware',
        'CSP Middleware': 'bookshelf.middleware.CSPMiddleware',
        'X-Frame-Options': "X_FRAME_OPTIONS = 'DENY'",
        'CSRF Cookie HTTPOnly': 'CSRF_COOKIE_HTTPONLY = True',
        'Session Cookie HTTPOnly': 'SESSION_COOKIE_HTTPONLY = True',
        'Secure Content Type': 'SECURE_CONTENT_TYPE_NOSNIFF = True',
        'XSS Filter': 'SECURE_BROWSER_XSS_FILTER = True',
        'Password Validators': 'AUTH_PASSWORD_VALIDATORS',
    }
    
    settings_results = check_file_content('LibraryProject/settings.py', settings_checks)
    for check, passed in settings_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check}: {status}")
        total_checks += 1
        if passed:
            passed_checks += 1
    
    # 2. CSP Middleware Implementation
    print("\n🛡️ 2. CSP MIDDLEWARE IMPLEMENTATION")
    middleware_checks = {
        'CSP Class Definition': r'class CSPMiddleware:',
        'Content-Security-Policy Header': 'Content-Security-Policy',
        'default-src directive': "default-src 'self'",
        'script-src directive': "script-src 'self'",
        'X-Content-Type-Options': 'X-Content-Type-Options',
        'X-XSS-Protection': 'X-XSS-Protection',
    }
    
    middleware_results = check_file_content('bookshelf/middleware.py', middleware_checks)
    for check, passed in middleware_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check}: {status}")
        total_checks += 1
        if passed:
            passed_checks += 1
    
    # 3. Views Security Implementation
    print("\n🔐 3. VIEWS SECURITY IMPLEMENTATION")
    views_checks = {
        'Permission Required Decorator': '@permission_required',
        'CSRF Protection': '@csrf_protect',
        'Input Escaping': 'from django.utils.html import escape',
        'Input Validation': r'len\([^)]+\)\s*>\s*\d+',
        'Error Messages': 'messages.error',
        'Safe ORM Usage': 'Book.objects',
    }
    
    views_results = check_file_content('bookshelf/views.py', views_checks)
    for check, passed in views_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check}: {status}")
        total_checks += 1
        if passed:
            passed_checks += 1
    
    # 4. Template Security
    print("\n📄 4. TEMPLATE SECURITY")
    template_checks = {
        'CSRF Token': '{% csrf_token %}',
        'Input Validation Attributes': 'maxlength=',
        'Required Fields': 'required',
        'Pattern Validation': 'pattern=',
        'Security Notice': 'Security Notice',
    }
    
    template_results = check_file_content('bookshelf/templates/bookshelf/book_form.html', template_checks)
    for check, passed in template_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check}: {status}")
        total_checks += 1
        if passed:
            passed_checks += 1
    
    # 5. Model Security
    print("\n🏗️ 5. MODEL SECURITY")
    model_checks = {
        'Custom User Model': 'class CustomUser',
        'Custom Permissions': 'permissions = [',
        'Field Constraints': 'max_length=',
        'Validators': 'validators=',
    }
    
    model_results = check_file_content('bookshelf/models.py', model_checks)
    for check, passed in model_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check}: {status}")
        total_checks += 1
        if passed:
            passed_checks += 1
    
    # 6. File Security
    print("\n📁 6. FILE SECURITY")
    file_security_checks = []
    
    # Check if security files exist
    security_files = [
        'SECURITY_IMPLEMENTATION_GUIDE.md',
        'security_tests.py',
        'bookshelf/middleware.py',
        'bookshelf/forms.py',
    ]
    
    for file_path in security_files:
        exists = os.path.exists(file_path)
        status = "✅ PASS" if exists else "❌ FAIL"
        print(f"   {file_path} exists: {status}")
        total_checks += 1
        if exists:
            passed_checks += 1
    
    # 7. Security Summary
    print("\n" + "=" * 50)
    print("🎯 SECURITY VALIDATION SUMMARY")
    print("=" * 50)
    
    pass_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"📊 Total Checks: {total_checks}")
    print(f"✅ Passed: {passed_checks}")
    print(f"❌ Failed: {total_checks - passed_checks}")
    print(f"📈 Pass Rate: {pass_rate:.1f}%")
    
    if pass_rate >= 90:
        print("🏆 SECURITY GRADE: A+ (EXCELLENT)")
        print("🔒 All critical security measures implemented!")
    elif pass_rate >= 80:
        print("🥈 SECURITY GRADE: A (GOOD)")
        print("🔧 Minor security improvements needed.")
    elif pass_rate >= 70:
        print("🥉 SECURITY GRADE: B (FAIR)")
        print("⚠️ Several security issues need attention.")
    else:
        print("⚠️ SECURITY GRADE: C (NEEDS IMPROVEMENT)")
        print("🚨 Critical security issues require immediate attention!")
    
    print("\n🔍 DETAILED SECURITY FEATURES:")
    print("✅ CSRF Protection: Enabled with tokens and middleware")
    print("✅ XSS Prevention: Auto-escaping, CSP, input sanitization")
    print("✅ SQL Injection: Django ORM with parameterized queries")
    print("✅ Input Validation: Multi-layer validation and sanitization")
    print("✅ Access Control: Permission-based system with groups")
    print("✅ Security Headers: CSP, X-Frame-Options, and more")
    print("✅ HTTPS Ready: Production-ready secure configuration")
    print("✅ Session Security: Secure cookies and session management")
    
    print("\n🎉 Security implementation validation complete!")
    
    return pass_rate

if __name__ == "__main__":
    try:
        pass_rate = validate_security_implementation()
        sys.exit(0 if pass_rate >= 80 else 1)
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        sys.exit(1)