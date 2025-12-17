<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '../store/auth.store'
import { useRouter } from 'vue-router'

import InputField from '../components/InputField.vue'
import PasswordField from '../components/PasswordField.vue'

const auth = useAuthStore()
const router = useRouter()

const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

const errorMessage = ref('')

/**
 * Tenta realizar a autenticação.
 * O fluxo agora lida com o login (POST) e a busca de perfil (GET /usuarios/).
 */
const submit = async () => {
  errorMessage.value = ''
  try {
    // 1. Envia as credenciais para a store
    await auth.login(form.email, form.password)
    
    // 2. Se o login e a busca de perfil funcionarem, redireciona para a home
    router.push('/')
  } catch (e: any) {
    // 3. Tratamento de erro detalhado:
    
    // Erro 401 ou 400 vindo do Backend (ex: "Usuário inativo" ou "Senha incorreta")
    if (e.response?.data?.detail) {
      errorMessage.value = e.response.data.detail
    } 
    // Erro lançado pela Store no fetchMe (ex: "Usuário não encontrado na listagem")
    else if (e.message) {
      errorMessage.value = e.message
    } 
    // Erro de conexão ou rede
    else {
      errorMessage.value = 'Erro de conexão com o servidor. Tente novamente.'
    }
  }
}
</script>

<template>
  <div class="login-container">
    <div class="logo-area">
      <img src="../assets/UFC_logo.png" alt="Logo UFC" />
    </div>

    <div class="login-card">
      <h1>Login</h1>

      <InputField
        label="Email"
        v-model="form.email"
        type="email"
        placeholder="Digite seu email"
      />

      <PasswordField
        label="Senha"
        v-model="form.password"
        placeholder="Digite sua senha"
      />

      <div class="options-row">
        <label class="checkbox-container">
          <input type="checkbox" v-model="form.rememberMe" />
          Lembrar de mim
        </label>

        <router-link to="/forgot-password" class="link">
          Esqueceu a senha?
        </router-link>
      </div>

      <p v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </p>

      <button @click="submit" :disabled="auth.loading">
        {{ auth.loading ? 'Aguarde...' : 'Entrar' }}
      </button>

      <p class="register-text">
        Não tem uma conta?
        <router-link to="/register" class="link register-link">
          Registre-se aqui
        </router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 120px;
  padding: 20px;
  min-height: 100vh;
}

.login-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 380px;
  background: #ffffff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
}

.logo-area img {
  width: 280px;
  max-width: 100%;
  object-fit: contain;
}

.login-card h1 {
  text-align: center;
  font-size: 26px;
  margin-bottom: 10px;
  color: #333;
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
  transition: 0.2s ease;
}

button:hover {
  background-color: #7a040a;
}

button:active {
  transform: scale(0.97);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  margin-top: -8px;
}

.link {
  color: #9c060d;
  text-decoration: none;
  cursor: pointer;
}

.link:hover {
  text-decoration: underline;
}

.register-text {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.register-link {
  font-weight: bold;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
}

.error-message {
  color: #d93025;
  background-color: #ffe8e8;
  padding: 8px;
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
  margin: 0;
}
</style>