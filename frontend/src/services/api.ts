// src/services/api.ts
import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
})

// Interceptor para enviar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default api