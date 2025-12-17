import { defineStore } from 'pinia'
import { api } from '../services/api' 
import { RoleEnum } from '../types/roles' 

export interface User {
    id: number
    email: string 
    nome: string
    role: RoleEnum
    is_active: boolean
    orientador_id?: number | null
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
        isAuthenticated: (state) => !!state.token,
        isPublisher: (state) => {
            if (!state.user?.role) return false
            const publisherRoles = [RoleEnum.PROFESSOR, RoleEnum.BOLSISTA, RoleEnum.ADMIN]
            return publisherRoles.includes(state.user.role)
        },
        userRole: (state) => state.user?.role || null,
    },

    actions: {
        /**
         * Busca os dados do usuário logado.
         * Como o endpoint /me não existe no backend, filtramos a lista geral pelo e-mail salvo.
         */
        async fetchMe() {
            try {
                const response = await api.get<User[]>('/usuarios/')
                const savedEmail = localStorage.getItem('user_email')
                
                const currentUser = response.data.find(u => u.email === savedEmail)
                
                if (currentUser) {
                    this.user = currentUser
                } else {
                    throw new Error("Usuário não encontrado na listagem")
                }
            } catch (error) {
                this.logout()
                throw error
            }
        },

        async login(emailInput: string, passwordInput: string) {
            this.loading = true
            try {
                const formData = new URLSearchParams()
                formData.append('username', emailInput) 
                formData.append('password', passwordInput)

                const response = await api.post('/auth/login', formData, {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })

                const token = response.data.access_token
                this.token = token
                
                // Armazenamos o token e o email para recuperar os dados no fetchMe
                localStorage.setItem('token', token) 
                localStorage.setItem('user_email', emailInput)

                await this.fetchMe() 
            } catch (error: any) {
                this.logout()
                throw error
            } finally {
                this.loading = false
            }
        },

        async initializeStore() {
            if (this.token && !this.user) {
                try {
                    await this.fetchMe()
                } catch (e) {
                    this.logout()
                }
            }
        },

        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            localStorage.removeItem('user_email')
        }
    }
})