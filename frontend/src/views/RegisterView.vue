<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import InputField from '../components/InputField.vue'
import PasswordField from '../components/PasswordField.vue'
import UserTypeSelector from '../components/UserTypeSelector.vue'

import { api } from '../services/api'
import { useRouter } from 'vue-router'
import { RoleEnum, ROLE_OPTIONS } from '../types/roles'

const router = useRouter()

// Estado do formulário
const form = reactive({
  nome: '',
  email: '',  
  senha: '',
  confirmarSenha: '',
  role: RoleEnum.LEITOR,
  email_orientador: '',
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Computeds
const isBolsista = computed(() => form.role === RoleEnum.BOLSISTA)
const isProfessor = computed(() => form.role === RoleEnum.PROFESSOR)
const passwordsMatch = computed(() => form.senha === form.confirmarSenha)

// Nova computed property para verificar o domínio (opcional, mas limpa o código)
const emailHasCorrectDomain = computed(() => {
    if (isProfessor.value) {
        return form.email.toLowerCase().endsWith('@ufc.br')
    }
    // Para outras roles, a validação é sempre True
    return true; 
});

// Função de registro
async function registerUser() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.nome || !form.email || !form.senha || !form.confirmarSenha) {
    errorMessage.value = 'Por favor, preencha todos os campos obrigatórios.'
    return
  }

  if (!passwordsMatch.value) {
    errorMessage.value = 'As senhas não coincidem.'
    return
  }

  if (isBolsista.value && !form.email_orientador) {
    errorMessage.value = 'O e-mail do orientador é obrigatório para bolsistas.'
    return
  }

  if (isProfessor.value && !emailHasCorrectDomain.value) {
    errorMessage.value = 'Para se cadastrar como Professor, você deve usar um e-mail institucional (@ufc.br).'
    return
  }

  loading.value = true

  // Payload final enviado ao backend
  const payload: any = {
    nome: form.nome,
    email: form.email,
    senha: form.senha,
    role: form.role,
  }

  if (isBolsista.value) {
    payload.email_orientador = form.email_orientador
  }

  try {
    await api.post('/usuarios/', payload)

    if (isProfessor.value || isBolsista.value) {
      successMessage.value =
        'Cadastro realizado! Verifique seu e-mail (ou o do seu orientador) para ativação.'
    } else {
      successMessage.value = 'Conta criada com sucesso! Redirecionando para o login...'
      setTimeout(() => router.push('/login'), 2500)
    }
  } catch (error: any) {
      console.error('Erro no cadastro:', error.response?.data)
      // Tentativa de pegar a mensagem de erro do backend (ex: email já existe, erro de domínio do backend)
      errorMessage.value =
        error.response?.data?.detail || 
        error.response?.data?.[0]?.msg || // Se for erro de Pydantic como o que você viu
        'Erro inesperado ao criar conta.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="form-container">
    <div class="register-card">
      <h1>Criar Conta</h1>

      <UserTypeSelector v-model="form.role" :options="ROLE_OPTIONS" />

      <form @submit.prevent="registerUser">
        <InputField label="Nome Completo" v-model="form.nome" placeholder="Seu nome" required />

        <InputField
          label="Email"
          v-model="form.email"
          type="email"
          placeholder="Seu email"
          required
          :class="{ 'input-error': isProfessor && form.email.length > 0 && !emailHasCorrectDomain }"
        />

        <PasswordField label="Senha" v-model="form.senha" placeholder="Crie uma senha" required />

        <PasswordField
          label="Confirmar Senha"
          v-model="form.confirmarSenha"
          placeholder="Confirme a senha"
          :class="{ 'input-error': !passwordsMatch && form.confirmarSenha.length > 0 }"
          required
        />

        <InputField
          v-if="isBolsista"
          label="Email do Orientador"
          v-model="form.email_orientador"
          type="email"
          placeholder="Email do seu orientador"
          required
        />

        <p v-if="isProfessor && form.email.length > 0 && !emailHasCorrectDomain" class="error-message">
          O e-mail deve ser institucional (@ufc.br) para o perfil Professor.
        </p>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

        <button
          type="submit"
          :disabled="loading || !passwordsMatch || !form.nome || !form.email || !form.senha || (isBolsista && !form.email_orientador) || (isProfessor && !emailHasCorrectDomain)"
        >
          {{ loading ? 'Cadastrando...' : 'Registrar' }}
        </button>
      </form>

      <p class="login-text">
        Já tenho uma conta.
        <router-link to="/login" class="link">Voltar para o Login</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px 0;
}

.register-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 450px;
  background: #ffffff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
  font-family: Arial, Helvetica, sans-serif;
}

h1 {
  text-align: center;
  font-size: 26px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.link {
  color: #9c060d;
  text-decoration: none;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
}

.link:hover {
  text-decoration: underline;
}

.login-text {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.error-message {
  color: #d93025;
  background-color: #ffe8e8;
  padding: 8px;
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
}

.success-message {
  color: #155724;
  background-color: #d4edda;
  padding: 8px;
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
}

.input-error input {
  border-color: #d93025 !important;
}
</style>
