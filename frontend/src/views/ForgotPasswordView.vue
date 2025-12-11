<script setup lang="ts">
import { ref } from 'vue'
import InputField from '../components/InputField.vue'
import axios from 'axios'


const email = ref('')
const loading = ref(false)
const message = ref('')
const isError = ref(false)


// URL base do seu backend
const BASE_URL = 'http://localhost:8000/api/v1/auth'


async function recoverPassword() {
  if (!email.value) return


  loading.value = true
  message.value = ''
  isError.value = false


  try {
    // 1. CHAMA O ENDPOINT: POST /api/v1/auth/recover-password
    await axios.post(`${BASE_URL}/recover-password`, {
      email: email.value
    })


    message.value = 'Se o e-mail estiver cadastrado, você receberá um link de recuperação em breve.'
    email.value = '' // Limpa o campo
   
  } catch (error: any) {
    // Nota: O backend pode retornar 404, mas a mensagem de sucesso é mais segura
    console.error('Erro na recuperação:', error)
   
    // Deixando a mensagem de sucesso padrão para não dar dicas a invasores
    message.value = 'Se o e-mail estiver cadastrado, você receberá um link de recuperação em breve.'
   
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <div class="form-container">
    <div class="card">
      <img src="../assets/UFC_logo2.png" alt="" srcset="">
      <h1>Esqueci a Senha</h1>
      <p>Insira seu e-mail para que possamos enviar um link de redefinição.</p>


      <form @submit.prevent="recoverPassword">
        <InputField
          label="Email"
          v-model="email"
          type="email"
          placeholder="Seu e-mail cadastrado"
          required
        />


        <button type="submit" :disabled="loading">
          {{ loading ? 'Enviando...' : 'Enviar Link de Redefinição' }}
        </button>
      </form>
     
      <p v-if="message" :class="{'success': !isError, 'error': isError}">{{ message }}</p>


      <router-link to="/login" class="link back-link">Voltar para o Login</router-link>
    </div>
  </div>
</template>


<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}


.card {
  width: 380px;
  align-items: center;
  background: #ffffff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  gap: 16px;
}


img {
  width: 100px;
  margin-bottom: 10px;
}


h1 {
  font-size: 24px; text-align: center;
}


p {
  font-size: 14px; text-align: center; color: #666;
}


button {
  padding: 12px;
  border: none;
  border-radius: 6px;
  background-color: #9c060d;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 12px;
  transition: 0.2s ease;
}


.link {
  color: #9c060d;
  text-decoration: none;
  text-align: center;
}
.success { color: green; font-weight: bold; }
.error { color: red; font-weight: bold; }
</style>