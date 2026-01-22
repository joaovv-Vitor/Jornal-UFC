<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../store/auth.store'

const authStore = useAuthStore()

const anoAtual = computed(() => new Date().getFullYear())
</script>

<template>
  <footer class="footer">
    <div class="footer-content">

      <!-- COLUNA 1: IDENTIDADE -->
      <div class="footer-col">
        <h3 class="footer-title">Jornal UFC</h3>
        <p class="footer-text">
          Plataforma acadêmica de publicação e leitura de notícias,
          desenvolvida para fins educacionais.
        </p>
      </div>

      <!-- COLUNA 2: NAVEGAÇÃO -->
      <div class="footer-col">
        <h4 class="footer-subtitle">Navegação</h4>
        <ul class="footer-links">
          <li><router-link to="/">Feed</router-link></li>
          <li><router-link to="/categorias">Categorias</router-link></li>
          <li><router-link to="/noticias/criar" v-if="authStore.isPublisher">Publicar</router-link></li>
          <li><router-link to="/minhas-noticias" v-if="authStore.isPublisher">Minhas notícias</router-link></li>
        </ul>
      </div>

      <!-- COLUNA 3: CONTA -->
      <div class="footer-col">
        <h4 class="footer-subtitle">Conta</h4>
        <ul class="footer-links">
          <li v-if="!authStore.isAuthenticated">
            <router-link to="/login">Entrar</router-link>
          </li>
          <li v-else>
            <span class="user">Olá, {{ authStore.user?.nome }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- LINHA FINAL -->
    <div class="footer-bottom">
      <span>
        © {{ anoAtual }} Jornal UFC — Todos os direitos reservados
      </span>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 60px;
  background: #0b1f3a;
  color: #eaeaea;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 32px;
}

.footer-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #ffffff;
}

.footer-subtitle {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.footer-text {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #cfd8e3;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 8px;
}

.footer-links a {
  color: #cfd8e3;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #ffffff;
}

.user {
  font-size: 0.9rem;
  color: #cfd8e3;
}

.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding: 16px;
  text-align: center;
  font-size: 0.8rem;
  color: #b0c4de;
}
</style>
