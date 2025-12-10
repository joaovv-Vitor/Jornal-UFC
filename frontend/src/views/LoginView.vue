<script setup lang="ts">
    import InputField from '../components/InputField.vue';
    import PasswordField from '../components/PasswordField.vue';
    import { ref } from 'vue';
    import { useRouter } from 'vue-router'; 

    const email = ref('')
    const password = ref('')

    const router = useRouter()

    async function login() {
    if (!email.value || !password.value) {
        alert('Preencha todos os campos')
        return
    }

    // integrar com backend aqui
    console.log('Email:', email.value)
    console.log('Senha:', password.value)

    // simulação de sucesso
    router.push('/home')
}
</script>
<template>
    <div class="login-container">
    <h1>Login</h1>

    <InputField
      label="E-mail"
      v-model="email"
      placeholder="Digite seu e-mail"
    />

    <PasswordField
      label="Senha"
      v-model="password"
      placeholder="Digite sua senha"
    />

    <button class="login-btn" @click="login">
      Entrar
    </button>
  </div>

</template>
<style scoped>

  @import url('https://fonts.googleapis.com/css2?family=Anton&family=Baloo+2:wght@400..800&family=Baloo+Paaji+2:wght@400..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Merriweather:ital,opsz,wght@0,18..144,300..900;1,18..144,300..900&family=Orbitron:wght@400..900&family=Space+Grotesk:wght@300..700&display=swap');


  .login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: inter, Helvetica, sans-serif;
}
.login-container h1 {
  text-align: center;
}
.login-btn {
  padding: 12px;
  background: #9C060D;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}
</style>