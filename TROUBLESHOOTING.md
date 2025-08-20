# 🔧 Troubleshooting Guide

## ✅ Current Status: ALL SYSTEMS WORKING

Your BD Counselling Backend is now running successfully! Here's what's working:

### 🟢 **Working Endpoints:**
- ✅ **Health Check:** `http://localhost:8000/health/`
- ✅ **Root API:** `http://localhost:8000/`
- ✅ **Categories API:** `http://localhost:8000/api/categories/`
- ✅ **Admin Panel:** `http://localhost:8000/admin/` (redirects to login)
- ✅ **Swagger Docs:** `http://localhost:8000/swagger/`
- ✅ **ReDoc:** `http://localhost:8000/redoc/`

### 🟢 **Server Status:**
- ✅ Django server running on port 8000
- ✅ All migrations applied
- ✅ Static files collected
- ✅ Environment variables loaded correctly
- ✅ Database models working
- ✅ 2 superusers available in database

---

## 🚨 Common Issues & Solutions

### 1. **Server Won't Start**

**Problem:** `Error: That port is already in use`

**Solution:**
```bash
# Kill existing processes
pkill -f "python manage.py runserver"

# Or find and kill specific process
lsof -ti:8000 | xargs kill -9

# Then restart
python manage.py runserver 0.0.0.0:8000
```

### 2. **Admin Panel Issues**

**Problem:** "Session data corrupted" or admin not loading

**Solution:**
```bash
# Clear session data
python manage.py clearsessions

# Collect static files
python manage.py collectstatic --no-input

# Restart server
python manage.py runserver 0.0.0.0:8000
```

### 3. **Environment Variables Not Loading**

**Problem:** Settings not reading from .env file

**Solution:**
```bash
# Check if .env exists
ls -la .env

# Create .env if missing
python setup_env.py

# Or manually copy
cp env.example .env
```

### 4. **Database Issues**

**Problem:** Database errors or missing tables

**Solution:**
```bash
# Run migrations
python manage.py migrate

# Check database status
python manage.py check --database default

# Create superuser if needed
python manage.py createsuperuser
```

### 5. **API Endpoints Not Working**

**Problem:** 404 errors or empty responses

**Solution:**
```bash
# Check if server is running
curl http://localhost:8000/health/

# Check Django settings
python manage.py check

# Verify URLs are configured
python manage.py show_urls
```

---

## 🔍 **Diagnostic Commands**

### **Check Server Status:**
```bash
# Check if server is running
ps aux | grep "python manage.py runserver"

# Test health endpoint
curl http://localhost:8000/health/

# Check server logs
tail -f server.log
```

### **Check Database:**
```bash
# Check migrations
python manage.py showmigrations

# Check database connection
python manage.py check --database default

# Count records
python manage.py shell -c "from core.models import *; print('Allotment:', Allotment.objects.count())"
```

### **Check Environment:**
```bash
# Test environment variables
python -c "from decouple import config; print('SECRET_KEY:', bool(config('SECRET_KEY')))"

# Check Django settings
python manage.py check
```

---

## 🚀 **Quick Start Commands**

### **Start Development Server:**
```bash
# Option 1: Foreground (with logs)
python manage.py runserver 0.0.0.0:8000

# Option 2: Background (no logs)
python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

# Option 3: Background (with logs)
python manage.py runserver 0.0.0.0:8000 &
```

### **Stop Server:**
```bash
# Kill all Django processes
pkill -f "python manage.py runserver"

# Or kill specific port
lsof -ti:8000 | xargs kill -9
```

### **Restart Server:**
```bash
pkill -f "python manage.py runserver"
python manage.py runserver 0.0.0.0:8000 &
```

---

## 📊 **Current System Status**

| Component | Status | Details |
|-----------|--------|---------|
| **Django Server** | ✅ Running | Port 8000 |
| **Database** | ✅ Connected | SQLite with 6 users |
| **Admin Panel** | ✅ Working | 2 superusers available |
| **API Endpoints** | ✅ Working | All endpoints responding |
| **Static Files** | ✅ Collected | 202 files |
| **Environment** | ✅ Loaded | All variables working |
| **Migrations** | ✅ Applied | No pending migrations |

---

## 🎯 **Next Steps**

### **For Development:**
1. ✅ Server is running - you can now access all endpoints
2. Visit `http://localhost:8000/admin/` to access admin panel
3. Use the superuser credentials to log in
4. Test API endpoints with your frontend

### **For Production:**
1. Set up environment variables in Render
2. Deploy using the provided `render.yaml`
3. Configure email settings for production
4. Test all endpoints after deployment

---

## 📞 **Need Help?**

If you encounter any issues:

1. **Check this troubleshooting guide first**
2. **Run diagnostic commands above**
3. **Check server logs:** `tail -f server.log`
4. **Verify environment variables are set correctly**
5. **Ensure all dependencies are installed:** `pip install -r requirements.txt`

**Current Status: 🎉 ALL SYSTEMS OPERATIONAL!**
