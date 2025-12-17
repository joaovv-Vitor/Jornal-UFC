<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { Noticia } from '../../types/noticias'

const props = defineProps<{
  noticia: Noticia
}>()

const dataFormatada = computed(() => {
  return new Date(props.noticia.criado_em).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
})
</script>

<template>
  <article class="noticia-card">
    <RouterLink :to="`/noticias/${noticia.slug}`" class="card-link">
      
      <!-- Imagem de capa -->
      <img
        :src="noticia.imagem_capa"
        :alt="noticia.titulo"
        class="capa"
      />

      <!-- Conteúdo -->
      <div class="conteudo">
        <h2 class="titulo">{{ noticia.titulo }}</h2>

        <p v-if="noticia.subtitulo" class="subtitulo">
          {{ noticia.subtitulo }}
        </p>

        <div class="meta">
          <span class="autor">{{ noticia.autor?.nome }}</span>
          <span class="data">{{ dataFormatada }}</span>
        </div>

        <div v-if="noticia.tags?.length" class="tags">
          <span
            v-for="tag in noticia.tags"
            :key="tag.id"  class="tag"
          >
          #{{ tag.nome }} </span>
        </div>
      </div>

    </RouterLink>
  </article>
</template>

<style scoped>
.noticia-card {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.noticia-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.capa {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.conteudo {
  padding: 16px;
}

.titulo {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.subtitulo {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 12px;
}

.meta {
  font-size: 0.8rem;
  color: #777;
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 0.75rem;
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 999px;
}
</style>