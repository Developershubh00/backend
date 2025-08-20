# 🔧 Environment Variables Setup Guide

This guide explains how to set up environment variables for the BD Counselling Backend.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_env.py
```
This interactive script will guide you through setting up all environment variables and create a `.env` file automatically.

### Option 2: Manual Setup
```bash
cp env.example .env
# Edit .env file with your configuration
```

## 📋 Environment Variables Reference

### 🔐 Django Core Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Auto-generated | ✅ Yes |
| `DEBUG` | Enable debug mode | `True` | ✅ Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | ✅ Yes |

### 🗄️ Database Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///db.sqlite3` | ✅ Yes |

**Examples:**
- **SQLite (Development):** `sqlite:///db.sqlite3`
- **PostgreSQL (Production):** `postgresql://user:password@host:port/database`

### 🌐 CORS Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:5173,http://127.0.0.1:5173` | ✅ Yes |

**Examples:**
- **Development:** `http://localhost:5173,http://127.0.0.1:5173`
- **Production:** `https://your-frontend.onrender.com,https://your-domain.com`

### 📧 Email Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_BACKEND` | Email backend class | `django.core.mail.backends.console.EmailBackend` | ❌ No |
| `EMAIL_HOST` | SMTP server host | `smtp.gmail.com` | ❌ No |
| `EMAIL_PORT` | SMTP server port | `587` | ❌ No |
| `EMAIL_USE_TLS` | Use TLS encryption | `True` | ❌ No |
| `EMAIL_HOST_USER` | Email username | `` | ❌ No |
| `EMAIL_HOST_PASSWORD` | Email password/app password | `` | ❌ No |

**Gmail Setup Example:**
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note:** For Gmail, you need to use an "App Password" instead of your regular password.

### 🔐 JWT Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `JWT_ACCESS_TOKEN_LIFETIME` | Access token lifetime in minutes | `60` | ❌ No |
| `JWT_REFRESH_TOKEN_LIFETIME` | Refresh token lifetime in minutes | `1440` | ❌ No |

### 🔒 Security Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `False` (dev) / `True` (prod) | ❌ No |
| `SESSION_COOKIE_SECURE` | Secure session cookies | `False` (dev) / `True` (prod) | ❌ No |
| `CSRF_COOKIE_SECURE` | Secure CSRF cookies | `False` (dev) / `True` (prod) | ❌ No |

### 📁 Static & Media Files

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `STATIC_URL` | Static files URL prefix | `/static/` | ❌ No |
| `MEDIA_URL` | Media files URL prefix | `/media/` | ❌ No |

### 👨‍💼 Admin Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ADMIN_EMAIL` | Admin email address | `admin@example.com` | ❌ No |
| `ADMIN_USERNAME` | Admin username | `admin` | ❌ No |

## 🎯 Environment-Specific Configurations

### Development Environment
```bash
# .env for development
SECRET_KEY=your-dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Production Environment
```bash
# .env for production
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com,your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com,https://your-domain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🔧 Render Deployment

For Render deployment, set these environment variables in the Render dashboard:

### Required Variables
- `SECRET_KEY` - Generate a secure key
- `DEBUG` - Set to `false`
- `ALLOWED_HOSTS` - Set to `.onrender.com`
- `CORS_ALLOWED_ORIGINS` - Your frontend URL
- `DATABASE_URL` - Auto-set by Render

### Optional Variables
- `EMAIL_BACKEND` - `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST` - `smtp.gmail.com`
- `EMAIL_PORT` - `587`
- `EMAIL_USE_TLS` - `true`
- `EMAIL_HOST_USER` - Your email
- `EMAIL_HOST_PASSWORD` - Your app password
- `JWT_ACCESS_TOKEN_LIFETIME` - `60`
- `JWT_REFRESH_TOKEN_LIFETIME` - `1440`
- `SECURE_SSL_REDIRECT` - `true`
- `SESSION_COOKIE_SECURE` - `true`
- `CSRF_COOKIE_SECURE` - `true`

## 🔐 Security Best Practices

### 1. Secret Key Generation
```python
# Generate a secure secret key
import secrets
import string

alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
print(secret_key)
```

### 2. Email Security
- Use app passwords for Gmail
- Never commit email passwords to version control
- Use environment variables for all sensitive data

### 3. Production Security
- Set `DEBUG=False` in production
- Use HTTPS in production
- Enable secure cookies in production
- Use strong secret keys

## 🚨 Troubleshooting

### Common Issues

1. **Environment Variables Not Loading**
   - Ensure `.env` file is in the project root
   - Check file permissions
   - Verify variable names match exactly

2. **Email Not Working**
   - Check SMTP settings
   - Verify app password for Gmail
   - Test with console backend first

3. **CORS Errors**
   - Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
   - Check for trailing slashes
   - Ensure protocol (http/https) matches

4. **Database Connection**
   - Verify `DATABASE_URL` format
   - Check database credentials
   - Ensure database is accessible

### Validation Commands
```bash
# Check if .env is loaded
python -c "from decouple import config; print(config('SECRET_KEY', default='Not found'))"

# Test database connection
python manage.py check --database default

# Test email settings
python manage.py shell -c "from django.core.mail import send_mail; print('Email backend configured')"
```

## 📚 Additional Resources

- [Django Environment Variables](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [python-decouple Documentation](https://github.com/henriquebastos/python-decouple)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [Render Environment Variables](https://render.com/docs/environment-variables)
