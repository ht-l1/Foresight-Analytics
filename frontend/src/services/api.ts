import axios from 'axios';
import { ForecastResult, ApiResponse, DataPoint, FilterOptions } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
);

export const apiService = {
  // Health check
  async healthCheck(): Promise<any> {
    const response = await api.get('/health');
    return response.data;
  },

  // Get all data
  async getData(): Promise<ApiResponse<DataPoint[]>> {
    const response = await api.get('/data');
    return response.data;
  },

  // Filter data
  async filterData(filters: FilterOptions): Promise<ApiResponse<DataPoint[]>> {
    const response = await api.post('/data/filter', filters);
    return response.data;
  },

  // Generate forecast
  async generateForecast(params: {
    months: number;
    region?: string;
    category?: string;
  }): Promise<ApiResponse<ForecastResult>> {
    const response = await api.post('/forecast', params);
    return response.data;
  },
};

export default api;