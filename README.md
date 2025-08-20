# BD Counselling Backend

A Django REST API backend for the BD Counselling platform, designed to work with a React TypeScript frontend.

## Features

- JWT Authentication
- User management with custom user model
- College database management
- Seat matrix and cutoff data
- Rank predictor functionality
- FAQ management
- CORS enabled for frontend integration
- Swagger API documentation

## API Endpoints

### Authentication
- `POST /auth/signup/` - User registration
- `POST /auth/login/` - User login
- `POST /auth/token/refresh/` - Refresh JWT token
- `POST /auth/logout/` - User logout
- `GET /auth/profile/` - User profile
- `POST /auth/verify-email/` - Email verification

### Data Endpoints
- `GET /api/cutoffs/` - College cutoff data
- `GET /api/ug-seat-matrix/` - UG seat matrix
- `GET /api/pg-fee-details/` - PG fee details
- `GET /api/closing-ranks/` - Closing ranks
- `GET /api/private-colleges/` - Private colleges
- `GET /api/nirf-rankings/` - NIRF rankings
- `GET /api/allotments/` - Allotment data
- `GET /api/faqs/` - FAQ data
- `GET /medical-colleges/` - Medical colleges list
- `GET /rank-predictor/` - Rank predictor
- `GET /college-database/` - College database

### Documentation
- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc documentation

## Local Development

### Prerequisites
- Python 3.11+
- pip
- virtualenv (recommended)

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd bd_counselling_backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Option 1: Use the setup script (recommended)
python setup_env.py

# Option 2: Manual setup
cp env.example .env
# Edit .env with your local settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Deployment on Render

### Prerequisites
- Render account
- Git repository with your code

### Deployment Steps

1. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "Web Service"
   - Connect your Git repository

2. **Configure the Web Service:**
   - **Name:** `bd-counselling-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.wsgi:application`

3. **Set Environment Variables:**
   - `SECRET_KEY`: Generate a secure Django secret key
   - `DEBUG`: `false`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://your-frontend.onrender.com,http://localhost:5173`)
   - `DATABASE_URL`: Will be automatically set by Render

4. **Database Setup:**
   - Create a PostgreSQL database in Render
   - The `DATABASE_URL` will be automatically provided

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy your application

### Alternative: Using render.yaml

If you prefer using the `render.yaml` file:

1. Push your code with the `render.yaml` file to your repository
2. In Render dashboard, select "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically create the web service and database

## Frontend Integration

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://127.0.0.1:5173`
- Your production frontend domain

### API Base URL

For local development:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

For production:
```javascript
const API_BASE_URL = 'https://your-backend.onrender.com';
```

### Authentication

The API uses JWT tokens. Include the token in your requests:

```javascript
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
};
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Debug mode | `True` (dev) / `False` (prod) |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection string | SQLite (dev) / PostgreSQL (prod) |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `EMAIL_BACKEND` | Email backend | `django.core.mail.backends.console.EmailBackend` |
| `EMAIL_HOST` | Email host | `smtp.gmail.com` |
| `EMAIL_PORT` | Email port | `587` |
| `EMAIL_USE_TLS` | Use TLS for email | `True` |
| `EMAIL_HOST_USER` | Email username | Required for production |
| `EMAIL_HOST_PASSWORD` | Email password | Required for production |
| `JWT_ACCESS_TOKEN_LIFETIME` | JWT access token lifetime (minutes) | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME` | JWT refresh token lifetime (minutes) | `1440` |
| `SECURE_SSL_REDIRECT` | Enable SSL redirect | `False` (dev) / `True` (prod) |
| `SESSION_COOKIE_SECURE` | Secure session cookies | `False` (dev) / `True` (prod) |
| `CSRF_COOKIE_SECURE` | Secure CSRF cookies | `False` (dev) / `True` (prod) |
| `STATIC_URL` | Static files URL | `/static/` |
| `MEDIA_URL` | Media files URL | `/media/` |

## API Documentation

Once deployed, you can access:
- Swagger UI: `https://your-backend.onrender.com/swagger/`
- ReDoc: `https://your-backend.onrender.com/redoc/`

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure your frontend URL is in `CORS_ALLOWED_ORIGINS`
   - Check that `CORS_ALLOW_CREDENTIALS` is set to `True`

2. **Database Connection:**
   - Verify `DATABASE_URL` is correctly set
   - Ensure PostgreSQL is properly configured

3. **Static Files:**
   - Run `python manage.py collectstatic` before deployment
   - Ensure WhiteNoise is properly configured

4. **Environment Variables:**
   - Double-check all required environment variables are set
   - Ensure no trailing spaces in variable values

## Support

For issues and questions:
- Check the API documentation at `/swagger/`
- Review the Django logs in Render dashboard
- Ensure all environment variables are properly configured
