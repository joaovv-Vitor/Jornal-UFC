<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { buscarNoticia, atualizarNoticia } from '../../services/noticias.api'
import NoticiaForm from '../../components/noticias/NoticiaForm.vue'
import type { Noticia } from '../../types/noticias'

const route = useRoute()
const router = useRouter()

const noticiaParaEditar = ref<any>(null) // Usamos any aqui para facilitar a transformação
const loading = ref(true)
const saving = ref(false)
const error = ref('')

/**
 * Carrega a notícia e transforma os dados para o formato que o formulário aceita
 */
async function carregarDados() {
  try {
    loading.value = true
    const slug = route.params.slug as string 
    const response = await buscarNoticia(slug)
    const data = response.data

    noticiaParaEditar.value = {
      titulo: data.titulo,
      subtitulo: data.subtitulo,
      conteudo: data.conteudo,
      // 💡 Ajuste: Pega o ID de dentro do objeto categoria
      categoria_id: data.categoria?.id || null, 
      imagem_capa: data.imagem_capa,
      // 💡 Ajuste: Mapeia as tags de objetos para strings
      tags: data.tags ? data.tags.map((t: any) => t.nome) : []
    }
  } catch (e) {
    router.push('/')
  } finally {
    loading.value = false
  }
}

/**
 * Envia o FormData para o backend
 */
async function handleUpdate(formData: FormData) {
  saving.value = true
  error.value = ''
  
  try {
    const slugOriginal = route.params.slug as string
    // Buscamos o ID real da notícia que está no estado carregado
    const response = await buscarNoticia(slugOriginal)
    const id = response.data.id

    await atualizarNoticia(id, formData)
    
    // Redireciona para o feed ou para a própria notícia após salvar
    alert('Notícia atualizada com sucesso!')
    router.push('/') 
  } catch (e: any) {
    console.error("Erro ao atualizar:", e)
    error.value = e.response?.data?.detail || 'Erro ao atualizar a notícia no servidor.'
  } finally {
    saving.value = false
  }
}

onMounted(carregarDados)
</script>

<template>
  <div class="edit-view-container">
    <header class="header">
      <button @click="router.back()" class="back-btn">
        <span class="icon">←</span> Voltar
      </button>
      <h1>Editar Publicação</h1>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Buscando dados da notícia...</p>
    </div>

    <div v-else-if="noticiaParaEditar" class="form-card">
      <NoticiaForm 
        :initial-data="noticiaParaEditar" 
        :loading="saving" 
        @submit="handleUpdate" 
      />
      
      <div v-if="error" class="error-banner">
        {{ error }}
      </div>
    </div>

    <div v-else class="error-state">
      <p>Notícia não encontrada.</p>
      <button @click="router.push('/')">Voltar ao Feed</button>
    </div>
  </div>
</template>

<style scoped>
.edit-view-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.back-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  }
  .back-btn:hover {
  color: #f30606;
  }
h1 {
  font-size: 1.8rem;
  color: #ffffff;
  margin: 0;
}

.form-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.loading-state, .error-state {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.error-banner {
  margin-top: 20px;
  padding: 12px;
  background-color: #fce8e8;
  color: #d93025;
  border-radius: 6px;
  text-align: center;
  font-weight: bold;
}

/* Spinner Simples */
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #9c060d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>