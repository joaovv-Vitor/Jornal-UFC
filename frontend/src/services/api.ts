import axios from 'axios'
import { useAuthStore } from '../store/auth.store'
import router from '../router'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
})

// Interceptor de REQUISIÇÃO: Envia o token em todas as chamadas
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor de RESPOSTA: Lida com erros globais (Ex: Token expirado)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const authStore = useAuthStore()

    // Se o erro for 401 (Não autorizado), o token provavelmente expirou
    if (error.response?.status === 401) {
      authStore.logout() // Limpa o Pinia e o localStorage
      router.push('/login') // Redireciona para o login
    }

    return Promise.reject(error)
  }
)

export default api