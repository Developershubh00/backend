# BD Counselling Backend API Documentation

## Base URL
- **Development:** `http://localhost:8000`
- **Production:** `https://backend.onrender.com`

## Authentication
All API endpoints use JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### 1. User Registration
```http
POST /auth/signup/
```
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone": "+919876543210",
  "neet_rank": "15000",
  "category": "General",
  "state": "Maharashtra"
}
```
**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "phone": "+919876543210",
  "neet_rank": "15000",
  "category": "General",
  "state": "Maharashtra"
}
```

### 2. User Login
```http
POST /auth/login/
```
**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```
**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "username": "johndoe1234",
  "email": "john@example.com"
}
```

### 3. Token Refresh
```http
POST /auth/token/refresh/
```
**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. User Logout
```http
POST /auth/logout/
```
**Headers:** `Authorization: Bearer <token>`

### 5. User Profile
```http
GET /auth/profile/
```
**Headers:** `Authorization: Bearer <token>`

### 6. Email Verification
```http
POST /auth/verify-email/
```
**Request Body:**
```json
{
  "otp": "123456"
}
```

---

## 📊 Category-Based Data Endpoints

### 1. Get All Categories
```http
GET /api/categories/
```
**Response:**
```json
{
  "categories": [
    "All India Counseling - PG Medical",
    "Armed Forces Medical Services - AFMS (through MCC) - PG Medical",
    "Open States (Private Institute seats available for all candidates)",
    "Andhra Pradesh Government Quota - PG Medical",
    "Andhra Pradesh Management Quota - PG Medical",
    "Assam - PG Medical",
    "Bihar - PG Medical",
    "Chandigarh - PG Medical",
    "Chhattisgarh - PG Medical",
    "Delhi - PG Medical",
    "DNB Sponsored - PG Medical (Govt or PSU Inservice Candidates)",
    "Goa - PG Medical",
    "Gujarat - PG Medical",
    "Haryana - PG Medical",
    "Himachal Pradesh - PG Medical",
    "Jammu and Kashmir - PG Medical",
    "Jharkhand - PG Medical",
    "Karnataka - PG Medical",
    "Kerala - PG Medical",
    "Madhya Pradesh - PG Medical",
    "Maharashtra - PG Medical",
    "Manipur-JNIMS - PG Medical",
    "Manipur-RIMS - PG Medical",
    "NEIGRIHMS - PG Medical",
    "Odisha - PG Medical",
    "Pondicherry - PG Medical",
    "Punjab - PG Medical",
    "Rajasthan - PG Medical",
    "Sikkim - PG Medical",
    "Tamil Nadu Government Quota - PG Medical",
    "Tamil Nadu Management Quota - PG Medical",
    "Telangana Government Quota - PG Medical",
    "Telangana Management Quota - PG Medical",
    "Tripura - PG Medical",
    "Uttarakhand - PG Medical",
    "Uttar Pradesh - PG Medical",
    "West Bengal - PG Medical"
  ],
  "count": 37
}
```

### 2. Get Category Summary
```http
GET /api/category/summary/{category}/
```
**Example:** `GET /api/category/summary/All India Counseling - PG Medical/`

**Response:**
```json
{
  "category": "All India Counseling - PG Medical",
  "summary": {
    "allotments": 150,
    "closing_ranks": 200,
    "seat_matrix": 100,
    "fee_stipend_bond": 80
  },
  "total_records": 530
}
```

### 3. Get Allotments by Category
```http
GET /api/category/allotments/{category}/
```
**Example:** `GET /api/category/allotments/All India Counseling - PG Medical/`

**Response:**
```json
{
  "category": "All India Counseling - PG Medical",
  "count": 150,
  "data": [
    {
      "id": 1,
      "category": "All India Counseling - PG Medical",
      "round": "Round 1",
      "ai_rank": "150",
      "state": "Maharashtra",
      "institute": "AIIMS Delhi",
      "course": "MD General Medicine",
      "quota": "All India",
      "quota_category": "General",
      "fee": "50000",
      "stipend_year1": "80000",
      "bond_years": "3",
      "bond_penalty": "500000",
      "beds": "1000",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 4. Get Closing Ranks by Category
```http
GET /api/category/closing-ranks/{category}/
```
**Example:** `GET /api/category/closing-ranks/All India Counseling - PG Medical/`

**Response:**
```json
{
  "category": "All India Counseling - PG Medical",
  "count": 200,
  "data": [
    {
      "id": 1,
      "category": "All India Counseling - PG Medical",
      "quota": "All India",
      "quota_category": "General",
      "state": "Maharashtra",
      "institute": "AIIMS Delhi",
      "course": "MD General Medicine",
      "fee": "50000",
      "stipend_year1": "80000",
      "bond_years": "3",
      "bond_penalty": "500000",
      "beds": "1000",
      "cr_2023_1": "150",
      "cr_2023_2": "200",
      "cr_2023_3": "250",
      "cr_2023_4": "300",
      "cr_2023_5": "350",
      "cr_2024_1": "160",
      "cr_2024_2": "210",
      "cr_2024_3": "260",
      "cr_2024_4": "310",
      "cr_2024_5": "360",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 5. Get Seat Matrix by Category
```http
GET /api/category/seat-matrix/{category}/
```
**Example:** `GET /api/category/seat-matrix/All India Counseling - PG Medical/`

**Response:**
```json
{
  "category": "All India Counseling - PG Medical",
  "count": 100,
  "data": [
    {
      "id": 1,
      "category": "All India Counseling - PG Medical",
      "institute": "AIIMS Delhi",
      "program": "MD General Medicine",
      "quota": "All India",
      "open_seats": 50,
      "open_pwd": 5,
      "gen_ews": 10,
      "gen_ews_pwd": 1,
      "obc": 25,
      "obc_pwd": 3,
      "sc": 15,
      "sc_pwd": 2,
      "st": 8,
      "st_pwd": 1,
      "total_seats": 120,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 6. Get Fee, Stipend & Bond by Category
```http
GET /api/category/fee-stipend-bond/{category}/
```
**Example:** `GET /api/category/fee-stipend-bond/All India Counseling - PG Medical/`

**Response:**
```json
{
  "category": "All India Counseling - PG Medical",
  "count": 80,
  "data": [
    {
      "id": 1,
      "category": "All India Counseling - PG Medical",
      "state": "Maharashtra",
      "institute": "AIIMS Delhi",
      "course": "MD General Medicine",
      "quota": "All India",
      "fee": "50000",
      "stipend_year1": "80000",
      "bond_years": "3",
      "bond_penalty": "500000",
      "beds": "1000",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## 📚 Other Data Endpoints

### 1. Medical Colleges List
```http
GET /medical-colleges/
```

### 2. Rank Predictor
```http
GET /rank-predictor/
```

### 3. College Database
```http
GET /college-database/
```

### 4. FAQs
```http
GET /api/faqs/
```

### 5. FAQ Categories
```http
GET /api/faq-categories/
```

---

## 🔧 Admin Endpoints

### 1. CSV Upload
```http
POST /api/upload/{type}/
```
**Headers:** `Authorization: Bearer <admin_token>`
**Form Data:**
- `file`: CSV file
- `category`: Exact category name from the list
- `replace`: "true" or "false" (optional, default: "true")

**Types:**
- `allotment` - Upload allotment data
- `closingrank` - Upload closing rank data
- `seatmatrix` - Upload seat matrix data
- `fee` - Upload fee, stipend, and bond data

**Example:**
```bash
curl -X POST \
  -H "Authorization: Bearer <admin_token>" \
  -F "file=@allotments.csv" \
  -F "category=All India Counseling - PG Medical" \
  -F "replace=true" \
  http://localhost:8000/api/upload/allotment/
```

---

## 📖 Documentation Endpoints

### 1. Swagger UI
```http
GET /swagger/
```

### 2. ReDoc
```http
GET /redoc/
```

### 3. Health Check
```http
GET /health/
```
**Response:**
```json
{
  "status": "healthy",
  "message": "BD Counselling Backend API is running",
  "version": "1.0.0"
}
```

---

## 🎯 Frontend Integration Examples

### React TypeScript Example

```typescript
// API Client
class BDCApiClient {
  private baseURL: string;
  private token: string | null;

  constructor() {
    this.baseURL = process.env.NODE_ENV === 'production' 
      ? 'https://your-backend.onrender.com' 
      : 'http://localhost:8000';
    this.token = localStorage.getItem('access_token');
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  // Get all categories
  async getCategories() {
    return this.request('/api/categories/');
  }

  // Get category summary
  async getCategorySummary(category: string) {
    return this.request(`/api/category/summary/${encodeURIComponent(category)}/`);
  }

  // Get allotments for a category
  async getCategoryAllotments(category: string) {
    return this.request(`/api/category/allotments/${encodeURIComponent(category)}/`);
  }

  // Get closing ranks for a category
  async getCategoryClosingRanks(category: string) {
    return this.request(`/api/category/closing-ranks/${encodeURIComponent(category)}/`);
  }

  // Get seat matrix for a category
  async getCategorySeatMatrix(category: string) {
    return this.request(`/api/category/seat-matrix/${encodeURIComponent(category)}/`);
  }

  // Get fee, stipend & bond for a category
  async getCategoryFeeStipendBond(category: string) {
    return this.request(`/api/category/fee-stipend-bond/${encodeURIComponent(category)}/`);
  }
}

// Usage in React component
const api = new BDCApiClient();

// Get all categories
const categories = await api.getCategories();

// Get data for a specific category
const category = "All India Counseling - PG Medical";
const summary = await api.getCategorySummary(category);
const allotments = await api.getCategoryAllotments(category);
const closingRanks = await api.getCategoryClosingRanks(category);
const seatMatrix = await api.getCategorySeatMatrix(category);
const feeData = await api.getCategoryFeeStipendBond(category);
```

---

## 🚨 Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created (for POST requests)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## 📝 Notes

1. **Category Names**: Use exact category names as returned by `/api/categories/`
2. **URL Encoding**: Category names with spaces should be URL-encoded
3. **Authentication**: Most endpoints require JWT authentication
4. **CORS**: Configured for frontend integration
5. **Rate Limiting**: Consider implementing rate limiting for production
6. **Pagination**: For large datasets, consider implementing pagination
