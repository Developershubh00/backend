#!/usr/bin/env python3
"""
Setup script to create .env file for BD Counselling Backend
This script will help you create a .env file with all necessary environment variables.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length=50):
    """Generate a secure Django secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create .env file with environment variables"""
    
    # Check if .env already exists
    env_path = Path('.env')
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    # Get user input for configuration
    print("\n🔧 BD Counselling Backend Environment Setup")
    print("=" * 50)
    
    # Debug mode
    debug = input("Enable DEBUG mode? (y/N): ").lower() == 'y'
    
    # Allowed hosts
    allowed_hosts = input("Enter allowed hosts (comma-separated, default: localhost,127.0.0.1): ").strip()
    if not allowed_hosts:
        allowed_hosts = "localhost,127.0.0.1"
    
    # CORS origins
    cors_origins = input("Enter CORS allowed origins (comma-separated, default: http://localhost:5173,http://127.0.0.1:5173): ").strip()
    if not cors_origins:
        cors_origins = "http://localhost:5173,http://127.0.0.1:5173"
    
    # Database URL
    database_url = input("Enter database URL (default: sqlite:///db.sqlite3): ").strip()
    if not database_url:
        database_url = "sqlite:///db.sqlite3"
    
    # Email configuration
    print("\n📧 Email Configuration:")
    email_backend = input("Email backend (default: django.core.mail.backends.console.EmailBackend): ").strip()
    if not email_backend:
        email_backend = "django.core.mail.backends.console.EmailBackend"
    
    email_host = input("Email host (default: smtp.gmail.com): ").strip()
    if not email_host:
        email_host = "smtp.gmail.com"
    
    email_port = input("Email port (default: 587): ").strip()
    if not email_port:
        email_port = "587"
    
    email_use_tls = input("Use TLS? (y/N): ").lower() == 'y'
    
    email_user = input("Email username: ").strip()
    email_password = input("Email password: ").strip()
    
    # JWT settings
    print("\n🔐 JWT Settings:")
    jwt_access_lifetime = input("JWT access token lifetime in minutes (default: 60): ").strip()
    if not jwt_access_lifetime:
        jwt_access_lifetime = "60"
    
    jwt_refresh_lifetime = input("JWT refresh token lifetime in minutes (default: 1440): ").strip()
    if not jwt_refresh_lifetime:
        jwt_refresh_lifetime = "1440"
    
    # Security settings
    print("\n🔒 Security Settings:")
    secure_ssl_redirect = input("Enable SSL redirect? (y/N): ").lower() == 'y'
    session_cookie_secure = input("Secure session cookies? (y/N): ").lower() == 'y'
    csrf_cookie_secure = input("Secure CSRF cookies? (y/N): ").lower() == 'y'
    
    # Create .env content
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG={str(debug).lower()}
ALLOWED_HOSTS={allowed_hosts}

# Database Configuration
DATABASE_URL={database_url}

# CORS Settings
CORS_ALLOWED_ORIGINS={cors_origins}

# Email Settings
EMAIL_BACKEND={email_backend}
EMAIL_HOST={email_host}
EMAIL_PORT={email_port}
EMAIL_USE_TLS={str(email_use_tls).lower()}
EMAIL_HOST_USER={email_user}
EMAIL_HOST_PASSWORD={email_password}

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME={jwt_access_lifetime}
JWT_REFRESH_TOKEN_LIFETIME={jwt_refresh_lifetime}

# Security Settings
SECURE_SSL_REDIRECT={str(secure_ssl_redirect).lower()}
SESSION_COOKIE_SECURE={str(session_cookie_secure).lower()}
CSRF_COOKIE_SECURE={str(csrf_cookie_secure).lower()}

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Admin Settings
ADMIN_EMAIL=admin@example.com
ADMIN_USERNAME=admin
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 Location: {env_path.absolute()}")
        print("\n🔐 Generated Secret Key:", secret_key)
        print("\n⚠️  Important:")
        print("   - Keep your .env file secure and never commit it to version control")
        print("   - Update the secret key in production")
        print("   - Configure proper email settings for production")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    """Main function"""
    print("🚀 BD Counselling Backend Environment Setup")
    print("This script will help you create a .env file with all necessary configuration.")
    
    response = input("\nDo you want to proceed? (Y/n): ")
    if response.lower() in ['n', 'no']:
        print("❌ Setup cancelled.")
        return
    
    create_env_file()

if __name__ == "__main__":
    main()
