import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Crucial for sending/receiving HttpOnly cookies
});

// Request interceptor to attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  // Avoid attaching token to auth routes if needed, though usually harmless
  if (token && !config.url.startsWith('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for token rotation
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/auth/refresh')) {
      originalRequest._retry = true;
      try {
        // Attempt to refresh the token using the HttpOnly cookie
        const res = await axios.post(`${API_URL}/auth/refresh`, {}, { withCredentials: true });
        const newAccessToken = res.data.access_token;
        
        // Save the new token
        localStorage.setItem('access_token', newAccessToken);
        
        // Update the authorization header and retry the original request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails (e.g. refresh token expired), clear storage and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
