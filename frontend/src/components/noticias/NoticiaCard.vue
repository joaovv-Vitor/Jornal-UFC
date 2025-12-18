<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { Noticia } from '../../types/noticias'

const props = defineProps<{
  noticia: Noticia
}>()

// 💡 CORREÇÃO 1: Função para montar a URL completa da imagem
const getImageUrl = (path: string | undefined | null): string => {
  if (!path) return '' 
  if (path.startsWith('http')) return path
  // Garante que o caminho comece com / e concatena com o endereço do backend
  const cleanPath = path.startsWith('/') ? path : `/${path}`
  return `http://localhost:8000${cleanPath}`
}

const dataFormatada = computed(() => {
  if (!props.noticia.criado_em) return ''
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
      
      <img
        v-if="noticia.imagem_capa"
        :src="getImageUrl(noticia.imagem_capa)"
        :alt="noticia.titulo"
        class="capa"
      />
      <div v-else class="sem-capa">📰</div>

      <div class="conteudo">
        <h2 class="titulo">{{ noticia.titulo }}</h2>

        <p v-if="noticia.subtitulo" class="subtitulo">
          {{ noticia.subtitulo }}
        </p>

        <div class="meta">
          <span class="autor" v-if="noticia.autor?.nome">
            Por: {{ noticia.autor.nome }}
          </span>
          <span class="data">{{ dataFormatada }}</span>
        </div>

        <div v-if="noticia.tags?.length" class="tags">
          <span
            v-for="tag in noticia.tags"
            :key="tag.id" class="tag"
          >
            #{{ tag.nome }}
          </span>
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
  height: 100%; /* Garante que todos os cards tenham o mesmo tamanho no grid */
  display: flex;
}

.noticia-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.card-link {
  text-decoration: none;
  color: #333; /* Cor do texto mais escura para legibilidade */
  display: flex;
  flex-direction: column;
  width: 100%;
}

.capa {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.sem-capa {
  width: 100%;
  height: 200px;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.conteudo {
  padding: 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.titulo {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.subtitulo {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 12px;
  flex-grow: 1; /* Empurra a meta e tags para o final do card */
}

.meta {
  font-size: 0.8rem;
  color: #777;
  display: flex;
  justify-content: space-between; /* Autor de um lado, data do outro */
  margin-bottom: 12px;
  border-top: 1px solid #f5f5f5;
  padding-top: 10px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 0.7rem;
  background: #f0f0f0;
  color: #666;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 500;
}
</style>