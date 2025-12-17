<script setup lang="ts">
import { useAuthStore } from '../store/auth.store'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="feed-container">
    <nav class="navbar">
      <h1>Jornal UFC</h1>
      <div class="user-controls">
        <span v-if="authStore.user" class="user-name">
          Olá, {{ authStore.user.nome }}
        </span>
        
        <button 
          v-if="authStore.isAuthenticated" 
          @click="handleLogout" 
          class="btn-logout"
        >
          Sair
        </button>
        
        <router-link v-else to="/login" class="btn-login">
          Entrar
        </router-link>
      </div>
    </nav>

    <main class="content">
      <h2>Feed de Notícias</h2>
      <p v-if="!authStore.isAuthenticated">
        Faça login para ver notícias exclusivas.
      </p>
    </main>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.btn-logout {
  padding: 8px 16px;
  background-color: #9c060d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-logout:hover {
  background-color: #7a040a;
}

.btn-login {
  color: #9c060d;
  text-decoration: none;
  font-weight: bold;
}

.content {
  padding: 2rem;
}
</style>