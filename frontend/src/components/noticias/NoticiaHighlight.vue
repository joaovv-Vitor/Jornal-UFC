<script setup lang="ts">
import type { Noticia } from '../../types/noticias'

defineProps<{
  noticia: Noticia
}>()

const getImageUrl = (path?: string | null): string => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:8000${path.startsWith('/') ? '' : '/'}${path}`
}
</script>

<template>
  <router-link
    :to="`/noticias/${noticia.slug}`"
    class="highlight"
  >
    <img
      :src="getImageUrl(noticia.imagem_capa)"
      :alt="noticia.titulo"
      class="highlight-image"
    />

    <div class="overlay">
      <span v-if="noticia.categoria" class="categoria">
        {{ noticia.categoria.nome }}
      </span>

      <h2 class="titulo">{{ noticia.titulo }}</h2>

      <p v-if="noticia.subtitulo" class="subtitulo">
        {{ noticia.subtitulo }}
      </p>

      <div class="footer">
        <span class="autor">Por {{ noticia.autor?.nome || 'Autor' }}</span>
        <span class="data">
          {{ new Date(noticia.criado_em).toLocaleDateString('pt-BR') }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<style scoped>
.highlight {
  position: relative;
  display: block;
  width: 100%;
  height: 580px;
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.highlight-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;
  padding: 32px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: linear-gradient(
    to top,
    rgba(0,0,0,0.75),
    rgba(0,0,0,0.25),
    transparent
  );
  color: #fff;
}

.categoria {
  font-size: 0.75rem;
  font-weight: bold;
  color: #ffd1d1;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.titulo {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 6px;
}

.subtitulo {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 16px;
}

.footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  opacity: 0.85;
}
</style>
