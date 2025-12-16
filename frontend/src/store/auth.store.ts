import { defineStore } from 'pinia'
import api from '../services/api'

export interface User {
  id: number
  username: string
}

interface AuthState {
  token: string | null
  user: User | null
  loading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: null,
    loading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(username: string, password: string) {
      this.loading = true
      try {
        const response = await api.post('/auth/login', {
          username,
          password
        })

        const token = response.data.access_token as string

        this.token = token
        localStorage.setItem('token', token)

        await this.fetchMe()
      } catch (error) {
          this.token = null
          localStorage.removeItem('token')

          throw error
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      const response = await api.get('/auth/me')
      this.user = response.data
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
