// Example API client for React TypeScript frontend
// This file shows how to integrate with the BD Counselling Backend API

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend.onrender.com' 
  : 'http://localhost:8000';

class BDCApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  // Set auth token
  setToken(token) {
    this.token = token;
    localStorage.setItem('access_token', token);
  }

  // Clear auth token
  clearToken() {
    this.token = null;
    localStorage.removeItem('access_token');
  }

  // Get auth headers
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health/');
  }

  // Authentication endpoints
  async signup(userData) {
    return this.request('/auth/signup/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials) {
    const response = await this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (response.access) {
      this.setToken(response.access);
    }
    
    return response;
  }

  async logout() {
    const response = await this.request('/auth/logout/', {
      method: 'POST',
    });
    
    this.clearToken();
    return response;
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await this.request('/auth/token/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    if (response.access) {
      this.setToken(response.access);
    }
    
    return response;
  }

  async getProfile() {
    return this.request('/auth/profile/');
  }

  async verifyEmail(otp) {
    return this.request('/auth/verify-email/', {
      method: 'POST',
      body: JSON.stringify({ otp }),
    });
  }

  // Data endpoints
  async getCutoffs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/cutoffs/${queryString ? '?' + queryString : ''}`);
  }

  async getSeatMatrix(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/ug-seat-matrix/${queryString ? '?' + queryString : ''}`);
  }

  async getFeeDetails(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/pg-fee-details/${queryString ? '?' + queryString : ''}`);
  }

  async getClosingRanks(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/closing-ranks/${queryString ? '?' + queryString : ''}`);
  }

  async getPrivateColleges(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/private-colleges/${queryString ? '?' + queryString : ''}`);
  }

  async getNIRFRankings(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/nirf-rankings/${queryString ? '?' + queryString : ''}`);
  }

  async getAllotments(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/allotments/${queryString ? '?' + queryString : ''}`);
  }

  async getFAQs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/faqs/${queryString ? '?' + queryString : ''}`);
  }

  async getMedicalColleges(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/medical-colleges/${queryString ? '?' + queryString : ''}`);
  }

  async getRankPredictor(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/rank-predictor/${queryString ? '?' + queryString : ''}`);
  }

  async getCollegeDatabase(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/college-database/${queryString ? '?' + queryString : ''}`);
  }

  // Category-based endpoints
  async getCategories() {
    return this.request('/api/categories/');
  }

  async getCategorySummary(category) {
    return this.request(`/api/category/summary/${encodeURIComponent(category)}/`);
  }

  async getCategoryAllotments(category, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/category/allotments/${encodeURIComponent(category)}/${queryString ? '?' + queryString : ''}`);
  }

  async getCategoryClosingRanks(category, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/category/closing-ranks/${encodeURIComponent(category)}/${queryString ? '?' + queryString : ''}`);
  }

  async getCategorySeatMatrix(category, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/category/seat-matrix/${encodeURIComponent(category)}/${queryString ? '?' + queryString : ''}`);
  }

  async getCategoryFeeStipendBond(category, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/category/fee-stipend-bond/${encodeURIComponent(category)}/${queryString ? '?' + queryString : ''}`);
  }

  // User choices
  async getUserChoices() {
    return this.request('/api/choice-list/');
  }

  async addCollegeChoice(choiceData) {
    return this.request('/api/choice-list/', {
      method: 'POST',
      body: JSON.stringify(choiceData),
    });
  }

  async updateCollegeChoice(id, choiceData) {
    return this.request(`/api/choice-list/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(choiceData),
    });
  }

  async deleteCollegeChoice(id) {
    return this.request(`/api/choice-list/${id}/`, {
      method: 'DELETE',
    });
  }
}

// Export for use in React components
export default BDCApiClient;

// Usage examples:

/*
// In your React component:
import BDCApiClient from './api-client';

const api = new BDCApiClient();

// Login
const handleLogin = async (email, password) => {
  try {
    const response = await api.login({ email, password });
    console.log('Login successful:', response);
    // Handle successful login
  } catch (error) {
    console.error('Login failed:', error);
    // Handle login error
  }
};

// Get all categories
const fetchCategories = async () => {
  try {
    const categories = await api.getCategories();
    console.log('Categories:', categories);
    return categories.categories;
  } catch (error) {
    console.error('Failed to fetch categories:', error);
  }
};

// Get category data
const fetchCategoryData = async (category) => {
  try {
    // Get summary first
    const summary = await api.getCategorySummary(category);
    console.log('Category Summary:', summary);

    // Get all data types for the category
    const [allotments, closingRanks, seatMatrix, feeData] = await Promise.all([
      api.getCategoryAllotments(category),
      api.getCategoryClosingRanks(category),
      api.getCategorySeatMatrix(category),
      api.getCategoryFeeStipendBond(category)
    ]);

    console.log('Allotments:', allotments);
    console.log('Closing Ranks:', closingRanks);
    console.log('Seat Matrix:', seatMatrix);
    console.log('Fee Data:', feeData);

    return {
      summary,
      allotments,
      closingRanks,
      seatMatrix,
      feeData
    };
  } catch (error) {
    console.error('Failed to fetch category data:', error);
  }
};

// Example usage for "All India Counseling - PG Medical"
const loadAllIndiaData = async () => {
  const category = "All India Counseling - PG Medical";
  const data = await fetchCategoryData(category);
  
  // Now you can display this data in your frontend
  // data.allotments.data - Array of allotment records
  // data.closingRanks.data - Array of closing rank records
  // data.seatMatrix.data - Array of seat matrix records
  // data.feeData.data - Array of fee, stipend & bond records
};

// Health check
const checkApiHealth = async () => {
  try {
    const health = await api.healthCheck();
    console.log('API Health:', health);
  } catch (error) {
    console.error('API Health check failed:', error);
  }
};
*/
