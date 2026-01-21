<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { criarNoticia } from '../../services/noticias.api'
import NoticiasForm from '../../components/noticias/NoticiaForm.vue'
import BackButton from '../../components/BackButton.vue'

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
      <BackButton/>
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