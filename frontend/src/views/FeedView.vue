<script setup lang="ts">
import { ref, onMounted } from 'vue' // Adicionado ref e onMounted
import { useAuthStore } from '../store/auth.store'
import { useRouter } from 'vue-router'
import { listarNoticias } from '../services/noticias.api' // Adicionado service
import type { Noticia } from '../types/noticias' // Adicionado tipo

const authStore = useAuthStore()
const router = useRouter()

// --- ADIÇÕES DE ESTADO ---
const noticias = ref<Noticia[]>([])
const loading = ref(true)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// --- ADIÇÃO DE LÓGICA DE CARREGAMENTO ---
onMounted(async () => {
  try {
    const response = await listarNoticias()
    noticias.value = response.data
  } catch (error) {
    console.error("Erro ao carregar feed:", error)
  } finally {
    loading.value = false
  }
})

const getImageUrl = (path: string | undefined | null): string => {
  if (!path) return ''; // Retorna string vazia em vez de null
  if (path.startsWith('http')) return path;
  return `http://localhost:8000${path.startsWith('/') ? '' : '/'}${path}`;
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
        <router-link 
          v-if="authStore.isPublisher" 
          to="/noticias/criar" 
          class="btn-create"
        >
          + Nova Publicação
        </router-link>
        <router-link class="btn-myNotice" v-if="authStore.isPublisher" to="/minhas-noticias">
          Minhas Notícias
        </router-link>
        <router-link 
          v-if="authStore.isAdminOrProfessor" 
          to="/categorias" 
          class="btn-categorias"
        >
          Gerenciar Categorias
        </router-link>
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
      <header class="content-header">
        <h2>Feed de Notícias</h2>
      </header>

      <div v-if="loading" class="loading">Carregando notícias...</div>

      <div v-else class="noticias-grid">
        <article v-for="item in noticias" :key="item.id" class="noticia-card">
          <div class="card-image" v-if="item.imagem_capa">
            <img 
              :src="getImageUrl(item.imagem_capa)" 
              :alt="item.titulo" 
              class="img-capa"
            />
          </div>
          <div class="card-body">
            <span class="categoria" v-if="item.categoria">{{ item.categoria.nome }}</span>
            <h3>{{ item.titulo }}</h3>
            <p>{{ item.subtitulo || item.conteudo.substring(0, 100) + '...' }}</p>
            <router-link :to="`/noticias/${item.slug}`" class="read-more">Ler mais →</router-link>
          </div>
        </article>
      </div>

      <p v-if="!authStore.isAuthenticated && noticias.length === 0" class="empty-msg">
        Faça login para ver notícias exclusivas.
      </p>
    </main>
  </div>
</template>

<style scoped>

.btn-create {
  background-color: #28a745;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.9rem;
  margin-right: 10px;
}
.btn-myNotice {
  background-color: #023b79;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.9rem;
  margin-right: 10px;
}
.btn-categorias {
  background-color: #6f42c1;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.9rem;
  margin-right: 10px;
}
.content-header  {
  font-size: 1.5rem;
  margin-bottom: 20px;
  margin-left: 40%;
  color: #ffffff;
}

span.user-name {
  margin-right: 15px;
  font-weight: bolder;
}

.btn-logout {
  padding: 8px 16px;
  background-color: #9c060d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.noticias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
  margin-left: 20px;
}

.noticia-card {
  background: rgb(255, 255, 255);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

.card-image img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-body {
  padding: 15px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.categoria {
  color: #9c060d;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
}

h3 { margin: 10px 0; font-size: 1.2rem; color: #333; }
h1{color: rgb(0, 31, 71);}
p { color: #666; font-size: 0.9rem; margin-bottom: 15px; }


.read-more {
  margin-top: auto;
  color: #9c060d;
  font-weight: bold;
  text-decoration: none;
}

.loading { text-align: center; padding: 40px; color: #666; }

/* Mantendo seus estilos originais abaixo... */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* ... resto do seu CSS */
</style>