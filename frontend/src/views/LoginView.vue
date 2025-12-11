<script setup lang="ts">
import { reactive, ref } from 'vue'
import InputField from '../components/InputField.vue'
import PasswordField from '../components/PasswordField.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'


const router = useRouter()
const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})


const loading = ref(false)
const errorMessage = ref('')
const BASE_URL = 'http://localhost:8000/api/v1/auth'


async function submit() {
  loading.value = true
  errorMessage.value = ''


  // O endpoint do FastAPI espera 'username' e 'password' no formato form-data
  // (OAuth2PasswordRequestForm), não JSON. O Axios facilita o envio disso.
  const form_data = new URLSearchParams();
  form_data.append('username', form.email);
  form_data.append('password', form.password);


  try {
    // 1. Chamada de Login: POST /api/v1/auth/login
    const response = await axios.post(`${BASE_URL}/login`, form_data, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })


    // O backend retorna um Token (access_token)
    const token = response.data.access_token


    // 2. Armazenar o Token (usando localStorage/sessionStorage)
    // Se 'Lembrar de mim' estiver marcado, use localStorage, senão use sessionStorage.
    if (form.rememberMe) {
        localStorage.setItem('auth_token', token)
    } else {
        sessionStorage.setItem('auth_token', token)
    }


    // 3. Redirecionar para a área logada (ex: /dashboard ou /noticias)
    router.push('/home')


  } catch (error: any) {
    console.error('Erro de Login:', error)
    // Captura a mensagem de erro do FastAPI (detalhe)
    errorMessage.value = error.response?.data?.detail || 'Erro ao tentar logar. Verifique suas credenciais.'


  } finally {
    loading.value = false
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
          <span class="checkmark"></span>
        </label>
       
        <router-link to="/forgot-password" class="link">Esqueceu a senha?</router-link>
      </div>
     
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>


      <button @click="submit" :disabled="loading">
        {{ loading ? 'Aguarde...' : 'Entrar' }}
      </button>
     
      <p class="register-text">
        Não tem uma conta?
        <router-link to="/register" class="link register-link">Registre-se aqui</router-link>
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

/* Estilos de Checkbox simples */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
}

/* Estilo para a mensagem de erro */
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

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>