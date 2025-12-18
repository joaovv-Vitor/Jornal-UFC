// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../store/auth.store'
import LoginView from '../views/LoginView.vue'
import CriarNoticiaView from '../views/noticias/NoticiaCreateView.vue' // 💡 NOVA VIEW
import FeedView from '../views/FeedView.vue'

// Definição das roles necessárias para cada rota
interface RouteMeta {
    requiresAuth?: boolean;
    requiredPermission?: 'publisher' | 'admin'; // 'publisher' para Bolsista/Professor/Admin
}

const routes: RouteRecordRaw[] = [
    {
        path: '/login',
        name: 'login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('../views/RegisterView.vue')
    },
    {
        path: '/forgot-password',
        name: 'forgot-password',
        component: () => import('../views/ForgotPasswordView.vue')
    },
    {
        path: '/',
        name: 'feed',
        component: FeedView,
        meta: { requiresAuth: false } // O feed é público.
    },
    // 💡 NOVA ROTA: Criação de Notícias (Exige permissão de publicador)
    {
        path: '/noticias/criar',
        name: 'criar-noticia',
        component: CriarNoticiaView,
        meta: { requiresAuth: true, requiredPermission: 'publisher' }
    },
   {
    path: '/noticias/:slug',
    name: 'noticia-detalhe',
    component: () => import('../views/noticias/NoticiaDetalheView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 💡 GUARDA DE ROTAS: Lógica completa (Auth + Permissão)
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    const requiresAuth = to.meta.requiresAuth as boolean
    const requiredPermission = to.meta.requiredPermission as string | undefined

    // 1. Garante que os dados do usuário estejam carregados se houver token
    if (authStore.token && !authStore.user) {
        try {
            await authStore.fetchMe()
        } catch (e) {
            authStore.logout() // Token expirado ou inválido
            return next({ name: 'login', query: { redirect: to.fullPath } })
        }
    }
    
    // 2. Redirecionar usuários logados para a Home se tentarem acessar login/registro
    if ((to.name === 'login' || to.name === 'register' || to.name === 'forgot-password') && authStore.isAuthenticated) {
        return next({ name: 'feed' })
    }

    // 3. Checagem de Autenticação
    if (requiresAuth && !authStore.isAuthenticated) {
        // Redireciona para o login, salvando a rota original na query
        return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    // 4. Checagem de Permissão (Role)
    if (requiredPermission === 'publisher' && authStore.isAuthenticated) {
        // Usa o getter que criamos na Store para verificar se a role é suficiente
        if (!authStore.isPublisher) {
            alert('Acesso negado: Você não tem permissão para publicar notícias.')
            return next({ name: 'feed' }) // Redireciona para a home
        }
    }

    next() // Permite a navegação
})

export default router