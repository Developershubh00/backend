# Deployment Checklist for Render

## Pre-Deployment Checklist

### ✅ Code Preparation
- [ ] All code is committed to Git repository
- [ ] `requirements.txt` is up to date
- [ ] `render.yaml` is configured (optional)
- [ ] `build.sh` is executable
- [ ] Environment variables are documented in `env.example`

### ✅ Django Settings
- [ ] `DEBUG` is set to `False` for production
- [ ] `SECRET_KEY` is properly configured
- [ ] `ALLOWED_HOSTS` includes Render domain
- [ ] `CORS_ALLOWED_ORIGINS` includes frontend domain
- [ ] Database configuration uses `DATABASE_URL`
- [ ] Static files are configured with WhiteNoise
- [ ] Security settings are enabled for production

### ✅ Dependencies
- [ ] `gunicorn` is in requirements.txt
- [ ] `whitenoise` is in requirements.txt
- [ ] `dj-database-url` is in requirements.txt
- [ ] `psycopg2-binary` is in requirements.txt
- [ ] All other dependencies are listed

## Render Deployment Steps

### 1. Create Web Service
- [ ] Go to Render Dashboard
- [ ] Click "New +" → "Web Service"
- [ ] Connect your Git repository
- [ ] Select the repository branch

### 2. Configure Service
- [ ] **Name:** `bd-counselling-backend`
- [ ] **Environment:** `Python 3`
- [ ] **Build Command:** `pip install -r requirements.txt`
- [ ] **Start Command:** `gunicorn backend.wsgi:application`

### 3. Environment Variables
Set these in Render dashboard:
- [ ] `SECRET_KEY` = Generate a secure key
- [ ] `DEBUG` = `false`
- [ ] `ALLOWED_HOSTS` = `.onrender.com`
- [ ] `CORS_ALLOWED_ORIGINS` = Your frontend URL(s)
- [ ] `DATABASE_URL` = Will be auto-set by Render
- [ ] `EMAIL_BACKEND` = `django.core.mail.backends.smtp.EmailBackend`
- [ ] `EMAIL_HOST` = `smtp.gmail.com`
- [ ] `EMAIL_PORT` = `587`
- [ ] `EMAIL_USE_TLS` = `true`
- [ ] `EMAIL_HOST_USER` = Your email address
- [ ] `EMAIL_HOST_PASSWORD` = Your email app password
- [ ] `JWT_ACCESS_TOKEN_LIFETIME` = `60`
- [ ] `JWT_REFRESH_TOKEN_LIFETIME` = `1440`
- [ ] `SECURE_SSL_REDIRECT` = `true`
- [ ] `SESSION_COOKIE_SECURE` = `true`
- [ ] `CSRF_COOKIE_SECURE` = `true`
- [ ] `STATIC_URL` = `/static/`
- [ ] `MEDIA_URL` = `/media/`

### 4. Database Setup
- [ ] Create PostgreSQL database in Render
- [ ] Link database to web service
- [ ] Verify `DATABASE_URL` is automatically set

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor build logs for errors
- [ ] Wait for deployment to complete

## Post-Deployment Verification

### ✅ Health Check
- [ ] Visit `https://your-app.onrender.com/health/`
- [ ] Should return: `{"status": "healthy", "message": "BD Counselling Backend API is running", "version": "1.0.0"}`

### ✅ API Endpoints
- [ ] Test root endpoint: `https://your-app.onrender.com/`
- [ ] Test admin panel: `https://your-app.onrender.com/admin/`
- [ ] Test Swagger docs: `https://your-app.onrender.com/swagger/`

### ✅ Database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser if needed
- [ ] Verify data is accessible

### ✅ CORS
- [ ] Test API calls from frontend
- [ ] Verify CORS headers are present
- [ ] Check for CORS errors in browser console

### ✅ Authentication
- [ ] Test signup endpoint
- [ ] Test login endpoint
- [ ] Test JWT token generation
- [ ] Test protected endpoints

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Database Connection**
   - Verify `DATABASE_URL` is set correctly
   - Check PostgreSQL database is running
   - Ensure database credentials are correct

3. **CORS Errors**
   - Verify `CORS_ALLOWED_ORIGINS` includes frontend URL
   - Check `CORS_ALLOW_CREDENTIALS` is set to `True`
   - Ensure frontend is making requests to correct URL

4. **Static Files Not Loading**
   - Verify WhiteNoise is in `MIDDLEWARE`
   - Check `STATIC_ROOT` is set correctly
   - Ensure `collectstatic` was run during build

5. **Environment Variables**
   - Double-check all variables are set in Render
   - Verify no trailing spaces in values
   - Ensure `SECRET_KEY` is properly generated

## Frontend Integration

### Update Frontend Configuration
- [ ] Update API base URL to production URL
- [ ] Test all API endpoints from frontend
- [ ] Verify authentication flow works
- [ ] Check error handling for network issues

### Environment Variables for Frontend
```javascript
// In your React app
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend.onrender.com' 
  : 'http://localhost:8000';
```

## Monitoring

### Render Dashboard
- [ ] Monitor application logs
- [ ] Check resource usage
- [ ] Set up alerts for downtime
- [ ] Monitor database performance

### Application Health
- [ ] Set up health check monitoring
- [ ] Monitor API response times
- [ ] Track error rates
- [ ] Monitor user authentication success/failure

## Security Checklist

- [ ] `DEBUG` is set to `False`
- [ ] `SECRET_KEY` is secure and unique
- [ ] HTTPS is enforced
- [ ] CORS is properly configured
- [ ] Database credentials are secure
- [ ] Admin panel is protected
- [ ] JWT tokens are properly configured
- [ ] Input validation is in place
- [ ] Rate limiting is considered (if needed)
