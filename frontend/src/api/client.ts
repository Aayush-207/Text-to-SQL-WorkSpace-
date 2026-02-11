/**
 * API Client Configuration and Axios Instance
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIClient {
  private instance: AxiosInstance;

  constructor() {
    this.instance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    // Add response interceptor for error handling
    this.instance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle timeout
        if (error.code === 'ECONNABORTED') {
          console.error('Request timeout');
          return Promise.reject(new Error('Request timeout. Please try again.'));
        }

        // Handle network error
        if (!error.response) {
          console.error('Network error:', error.message);
          return Promise.reject(new Error('Network error. Please check your connection.'));
        }

        // Handle API error response
        const apiError = error.response.data as any;
        const message = apiError?.error || apiError?.detail || error.message;
        console.error('API Error:', message);
        return Promise.reject(new Error(message));
      }
    );
  }

  async get<T>(url: string, config?: any): Promise<T> {
    const response = await this.instance.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.instance.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.instance.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: any): Promise<T> {
    const response = await this.instance.delete<T>(url, config);
    return response.data;
  }
}

export const apiClient = new APIClient();
