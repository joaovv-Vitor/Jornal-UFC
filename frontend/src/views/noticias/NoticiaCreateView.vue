<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { criarNoticia } from '../../services/noticias.api'
import NoticiasForm from '../../components/noticias/NoticiaForm.vue'

const router = useRouter()
const loading = ref(false)
const error = ref('')

async function handleSubmit(formData: FormData) {
  loading.value = true
  error.value = ''
  
  try {
    // 💡 Seu service já está configurado para receber FormData e enviar o token
    await criarNoticia(formData)
    
    // Após criar, voltamos para o Feed (Home)
    router.push('/')
  } catch (e: any) {
    console.error(e)
    error.value = e.response?.data?.detail || 'Erro ao criar notícia. Verifique os campos.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="create-view-container">
    <div class="header">
      <button @click="router.back()" class="back-btn">← Voltar</button>
      <h1>Nova Publicação</h1>
    </div>

    <div class="form-card">
      <NoticiasForm 
        :loading="loading" 
        @submit="handleSubmit" 
      />
      
      <p v-if="error" class="error-msg">{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
  h1{
    color: white;
  }
.create-view-container {
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
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.error-msg {
  margin-top: 20px;
  color: #d93025;
  text-align: center;
  font-weight: bold;
}
</style>