<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth.store'
import { listarNoticias, deletarNoticia } from '../../services/noticias.api'
import NoticiaCard from '../../components/noticias/NoticiaCard.vue'
import DeleteConfirm from '../../components/noticias/DeleteConfirm.vue'
import type { Noticia } from '../../types/noticias'
import BackButton from '../../components/BackButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const noticias = ref<Noticia[]>([])
const loading = ref(true)

// Estado para controle do Modal de Exclusão
const showDeleteModal = ref(false)
const itemToDelete = ref<Noticia | null>(null)

function openDeleteModal(item: Noticia) {
  itemToDelete.value = item
  showDeleteModal.value = true
}

async function handleConfirmDelete() {
  if (!itemToDelete.value) return
  try {
    await deletarNoticia(itemToDelete.value.id)
    // Remove a notícia da lista localmente para não precisar recarregar tudo
    noticias.value = noticias.value.filter(n => n.id !== itemToDelete.value?.id)
    showDeleteModal.value = false
  } catch (error) {
    console.error('Erro ao excluir notícia:', error)
    alert('Erro ao excluir a notícia. Tente novamente.')
  }
}

onMounted(async () => {
  // Redireciona se não houver usuário (embora o guard de rotas já deva tratar isso)
  if (!authStore.user) {
    router.push('/login')
    return
  }

  try {
    loading.value = true
    // Busca todas as notícias
    const response = await listarNoticias()
    
    // Filtra localmente pelas notícias do usuário logado
    // Nota: Assumimos que a API retorna o objeto 'autor' com um 'id'
    const userId = authStore.user.id
    noticias.value = response.data.filter((n: any) => n.autor?.id === userId)
    
  } catch (error) {
    console.error('Erro ao carregar minhas notícias:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="minhas-noticias-view">
    <header class="view-header">
      <div class="title-group">
      
       <BackButton/>
        <h1>Minhas Publicações</h1>
      </div>
      
      <router-link to="/noticias/criar" class="btn-new">
        + Nova Notícia
      </router-link>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando suas publicações...</p>
    </div>

    <div v-else-if="noticias.length === 0" class="empty-state">
      <p>Você ainda não publicou nenhuma notícia.</p>
      <router-link to="/noticias/criar" class="link-cta">Começar a escrever</router-link>
    </div>

    <div v-else class="grid-container">
      <div v-for="item in noticias" :key="item.id" class="card-wrapper">
        <!-- Reutiliza o card do feed -->
        <NoticiaCard :noticia="item" />
        
        <!-- Ações exclusivas desta view -->
        <div class="actions">
            <button @click="openDeleteModal(item)" class="btn-delete">
                    Excluir
            </button>
            <router-link :to="`/noticias/${item.slug}/editar`" class="btn-edit">
                Editar
            </router-link>
          
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação -->
    <DeleteConfirm
      :show="showDeleteModal"
      title="Excluir Publicação"
      message="Tem certeza que deseja excluir esta notícia? Esta ação é irreversível."
      confirmText="Excluir"
      @confirm="handleConfirmDelete"
      @close="showDeleteModal = false"
    />
  </div>
</template>

<style scoped>
/* Container principal da página: limita a largura e centraliza */
.minhas-noticias-view {
  margin: 0 auto;
}
/* Cabeçalho da view: alinha o título e o botão de nova notícia */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  background-color: #ffffff;
  box-shadow: inset 0 -2px 4px rgba(0,0,0,0.1);
}

/* Agrupa o botão de voltar e o título h1 */
.title-group {
  display: flex;
  align-items: center;
  gap: 15px;
  
}
/* Botão verde para criar nova notícia */
.btn-new {
  background-color: #28a745;
  color: white;
  padding: 10px;
  margin-right: 10px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.2s;
}

.btn-new:hover {
  background-color: #218838;
}

/* Grid responsivo: ajusta colunas automaticamente (min 300px) */
.grid-container {
  display: grid;
  padding: 1px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

/* Wrapper individual de cada notícia (Card + Botões) */
.card-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Área de ações abaixo do card (ex: botão editar) */
.actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* Botão de editar (azul) */
.btn-edit {
  background-color: #0056b3;
  color: white;
  padding: 8px 0;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: bold;
  text-align: center;
  width: 100%;
  transition: background 0.2s;
}

.btn-edit:hover {
  background-color: #004494;
}

/* Botão de excluir (vermelho) */
.btn-delete {
  background-color: #dc3545;
  color: white;
  padding: 8px 0;
  border-radius: 4px;
  border: none;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete:hover {
  background-color: #c82333;
}

/* Estados de carregamento e lista vazia (centralizados e com fundo cinza claro) */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  background: #f9f9f9;
  border-radius: 8px;
  color: #666;
}

/* Animação de spinner para o loading */
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #fff6f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Link de chamada para ação (CTA) quando não há notícias */
.link-cta {
  color: #dd000b;
  font-weight: bold;
  text-decoration: none;
  margin-top: 10px;
  display: inline-block;
}
</style>
