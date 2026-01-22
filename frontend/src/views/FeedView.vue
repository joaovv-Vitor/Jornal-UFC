<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '../store/auth.store'
import { useRouter } from 'vue-router'
import { listarNoticias } from '../services/noticias.api'
import type { Noticia } from '../types/noticias'
import NoticiasCarousel from '../components/noticias/NoticiasCarousel.vue'

const authStore = useAuthStore()
const router = useRouter()

// --- ESTADOS ---
const noticias = ref<Noticia[]>([])
const loading = ref(true)
const loadingMais = ref(false)
const termoBusca = ref('')
const categoriaFiltro = ref('')

// Paginação
const skip = ref(0)
const LIMIT = 4 // Quantidade de notícias por página
const temMais = ref(true)

// --- LÓGICA DE FILTRO LOCAL (CLIENT-SIDE) ---
const noticiasFiltradas = computed(() => {
  return noticias.value.filter(noticia => {
    const termo = termoBusca.value.toLowerCase()
    const matchTexto = 
      noticia.titulo.toLowerCase().includes(termo) || 
      (noticia.subtitulo && noticia.subtitulo.toLowerCase().includes(termo))
    
    const matchCategoria = categoriaFiltro.value 
      ? noticia.categoria?.nome === categoriaFiltro.value 
      : true
      
    return matchTexto && matchCategoria
  })
})

const categoriasDisponiveis = computed(() => {
  const cats = new Set<string>()
  noticias.value.forEach(n => {
    if (n.categoria?.nome) cats.add(n.categoria.nome)
  })
  return Array.from(cats)
})

// --- CARREGAMENTO DE DADOS ---
async function carregarNoticias(acumular = false) {
  try {
    if (acumular) loadingMais.value = true
    else loading.value = true

    // Chamada para a API usando skip e limit
    const response = await listarNoticias({ 
      skip: skip.value, 
      limit: LIMIT 
    })
    
    const novasNoticias = response.data

    if (acumular) {
      noticias.value.push(...novasNoticias)
    } else {
      noticias.value = novasNoticias
    }

    // Se a API retornou menos que o limite, não há mais páginas
    temMais.value = novasNoticias.length === LIMIT
  } catch (error) {
    console.error("Erro ao carregar feed:", error)
  } finally {
    loading.value = false
    loadingMais.value = false
  }
}

async function handleCarregarMais() {
  skip.value += LIMIT
  await carregarNoticias(true)
}

// Reseta a paginação se o usuário começar a filtrar/buscar
watch([termoBusca, categoriaFiltro], () => {
  // Opcional: Se quiser fazer busca no servidor, chamaria carregarNoticias aqui.
  // Como o seu filtro é local, apenas escondemos o "Ver Mais" durante a busca 
  // para evitar inconsistências de interface.
})

onMounted(async () => {
  await carregarNoticias()
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const getImageUrl = (path: string | undefined | null): string => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:8000${path.startsWith('/') ? '' : '/'}${path}`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR')
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

        <router-link v-if="authStore.isPublisher" to="/noticias/criar" class="btn-create">
          + Nova Publicação
        </router-link>

        <router-link v-if="authStore.isPublisher" to="/minhas-noticias" class="btn-myNotice">
          Minhas Notícias
        </router-link>

        <router-link v-if="authStore.isAdminOrProfessor" to="/categorias" class="btn-categorias">
          Gerenciar Categorias
        </router-link>

        <button v-if="authStore.isAuthenticated" @click="handleLogout" class="btn-logout">
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

        <div class="filters">
          <input
            v-model="termoBusca"
            type="text"
            placeholder="Pesquisar nesta página..."
            class="search-input"
          />

          <select v-model="categoriaFiltro" class="cat-select">
            <option value="">Todas as Categorias</option>
            <option v-for="cat in categoriasDisponiveis" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>
      </header>

      <div v-if="loading" class="loading">
        Carregando notícias...
      </div>

      <div v-else>
        <NoticiasCarousel
          v-if="noticias.length && !termoBusca && !categoriaFiltro"
          :noticias="noticias.slice(0, 4)"
          :autoplay="true"
          :autoplayInterval="5000"
        />

        <div class="noticias-grid">
          <article
            v-for="item in noticiasFiltradas"
            :key="item.id"
            class="noticia-card"
          >
            <div class="card-image" v-if="item.imagem_capa">
              <img :src="getImageUrl(item.imagem_capa)" :alt="item.titulo" class="img-capa" />
            </div>
            <div class="card-body">
              <span class="categoria" v-if="item.categoria">
                {{ item.categoria.nome }}
              </span>

              <h3>{{ item.titulo }}</h3>

              <p>
                {{ item.subtitulo || item.conteudo.substring(0, 100) + '...' }}
              </p>

              <div class="card-footer">
                <router-link :to="`/noticias/${item.slug}`" class="read-more">
                  Ler mais →
                </router-link>
                <small class="date">{{ formatDate(item.criado_em) }}</small>
              </div>
            </div>
          </article>
        </div>

        <div class="pagination-area" v-if="!termoBusca && !categoriaFiltro">
          <button 
            v-if="temMais" 
            @click="handleCarregarMais" 
            class="btn-load-more"
            :disabled="loadingMais"
          >
            {{ loadingMais ? 'Carregando...' : 'Ver mais notícias' }}
          </button>
          <p v-else-if="noticias.length > 0" class="end-msg">
            Você viu todas as notícias por enquanto.
          </p>
        </div>
      </div>

      <div v-if="!loading && noticiasFiltradas.length === 0" class="empty-msg">
        <p v-if="authStore.isAuthenticated">Nenhuma notícia encontrada para os filtros selecionados.</p>
        <p v-else>Faça login para ver notícias exclusivas.</p>
      </div>
    </main>
  </div>
</template>


<style scoped>

.btn-create {
  background-color: #28a745;
  color: white;
  padding: 8px 5px;
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
  display: flex;
  flex-direction: column;
  align-items: center;   /* centraliza horizontalmente */
  justify-content: center;
  margin-bottom: 20px;
  color: #023b79;
}

.filters {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.search-input {
  width: 500px;
}

.search-input, .cat-select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
  
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
  max-width: calc(100% - 40px);
}

.noticia-card {
  background: rgb(255, 255, 255);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.noticia-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-4px);
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

h3 { margin: 10px 0; font-size: 1.2rem; color: #000000; }
h1{color: #023b79;}
p { color: #666; font-size: 0.9rem; margin-bottom: 15px; }
h2{padding: 10px;}


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

.pagination-area {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  width: 100%;
}

.btn-load-more {
  padding: 12px 30px;
  background-color: white;
  color: #023b79;
  border: 2px solid #023b79;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-load-more:hover:not(:disabled) {
  background-color: #023b79;
  color: white;
}

.btn-load-more:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.end-msg {
  color: #888;
  font-style: italic;
}
</style>