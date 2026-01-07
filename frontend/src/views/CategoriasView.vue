<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listarCategorias, criarCategoria, deletarCategoria } from '../services/categorias.api'
import type { Categoria } from '../types/categoria'

const router = useRouter()
const categorias = ref<Categoria[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')

// Formulário de criação
const showForm = ref(false)
const nomeCategoria = ref('')
const loadingCreate = ref(false)

// Carregar categorias
async function loadCategorias() {
  try {
    loading.value = true
    const response = await listarCategorias()
    categorias.value = response.data
  } catch (e: any) {
    error.value = 'Erro ao carregar categorias. Tente novamente.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

// Criar categoria
async function handleCreate() {
  if (!nomeCategoria.value.trim()) {
    error.value = 'O nome da categoria é obrigatório.'
    return
  }

  loadingCreate.value = true
  error.value = ''
  success.value = ''

  try {
    await criarCategoria(nomeCategoria.value.trim())
    success.value = 'Categoria criada com sucesso!'
    nomeCategoria.value = ''
    showForm.value = false
    await loadCategorias()
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Erro ao criar categoria. Verifique se já não existe uma categoria com esse nome.'
  } finally {
    loadingCreate.value = false
  }
}

// Deletar categoria
async function handleDelete(id: number, nome: string) {
  if (!confirm(`Tem certeza que deseja deletar a categoria "${nome}"?\n\nNotícias associadas a esta categoria não serão deletadas, apenas perderão a classificação.`)) {
    return
  }

  try {
    await deletarCategoria(id)
    success.value = 'Categoria deletada com sucesso!'
    await loadCategorias()
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Erro ao deletar categoria.'
  }
}

onMounted(() => {
  loadCategorias()
})
</script>

<template>
  <div class="categorias-container">
    <div class="header">
      <button @click="router.back()" class="back-btn">← Voltar</button>
      <h1>Gerenciar Categorias</h1>
    </div>

    <div class="form-card">
      <div class="form-header">
        <h2>Criar Nova Categoria</h2>
        <button 
          @click="showForm = !showForm" 
          class="toggle-btn"
          :class="{ active: showForm }"
        >
          {{ showForm ? '✕ Cancelar' : '+ Nova Categoria' }}
        </button>
      </div>

      <form v-if="showForm" @submit.prevent="handleCreate" class="create-form">
        <div class="field">
          <label>Nome da Categoria *</label>
          <input 
            v-model="nomeCategoria" 
            type="text" 
            placeholder="Ex: Tecnologia, Esportes, Educação..." 
            :disabled="loadingCreate"
          />
        </div>
        <button type="submit" :disabled="loadingCreate || !nomeCategoria.trim()">
          {{ loadingCreate ? 'Criando...' : 'Criar Categoria' }}
        </button>
      </form>
    </div>

    <div v-if="error" class="alert error">
      {{ error }}
    </div>
    <div v-if="success" class="alert success">
      {{ success }}
    </div>

    <div class="categorias-list">
      <h2>Categorias Existentes ({{ categorias.length }})</h2>
      
      <div v-if="loading" class="loading">Carregando categorias...</div>
      
      <div v-else-if="categorias.length === 0" class="empty">
        Nenhuma categoria cadastrada ainda.
      </div>

      <div v-else class="categorias-grid">
        <div v-for="categoria in categorias" :key="categoria.id" class="categoria-card">
          <div class="categoria-info">
            <h3>{{ categoria.nome }}</h3>
            <span class="slug">Slug: {{ categoria.slug }}</span>
          </div>
          <button 
            @click="handleDelete(categoria.id, categoria.nome)" 
            class="delete-btn"
            title="Deletar categoria"
          >
            🗑️ Deletar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.categorias-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.header h1 {
  color: white;
  margin: 0;
}

.back-btn {
  background-color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  color: #000;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.back-btn:hover {
  color: #f30606;
}

.form-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 20px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.form-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.toggle-btn {
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background-color: #218838;
}

.toggle-btn.active {
  background-color: #dc3545;
}

.toggle-btn.active:hover {
  background-color: #c82333;
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-weight: 600;
  color: #333;
}

.field input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.field input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.create-form button {
  padding: 12px;
  background-color: #9c060d;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  font-size: 15px;
}

.create-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-weight: 500;
}

.alert.error {
  background-color: #ffe8e8;
  color: #d93025;
  border: 1px solid #f5c6cb;
}

.alert.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.categorias-list {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.categorias-list h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.3rem;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.categorias-grid {
  display: grid;
  gap: 15px;
}

.categoria-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: box-shadow 0.2s;
}

.categoria-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.categoria-info {
  flex: 1;
}

.categoria-info h3 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 1.1rem;
}

.slug {
  font-size: 0.85rem;
  color: #666;
  font-family: monospace;
}

.delete-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background-color: #c82333;
}
</style>
