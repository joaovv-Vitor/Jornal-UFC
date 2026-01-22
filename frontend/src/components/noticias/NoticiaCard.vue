<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { Noticia } from '../../types/noticias'

const props = withDefaults(
  defineProps<{
    noticia: Noticia
    variant?: 'default' | 'carousel'
  }>(),
  {
    variant: 'default'
  }
)

const getImageUrl = (path: string | undefined | null): string => {
  if (!path) return ''
  if (path.startsWith('http')) return path
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
  <article class="noticia-card" :class="variant">
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

        <!-- Tags só aparecem fora do carrossel -->
        <div v-if="variant === 'default' && noticia.tags?.length" class="tags">
          <span
            v-for="tag in noticia.tags"
            :key="tag.id"
            class="tag"
          >
            #{{ tag.nome }}
          </span>
        </div>

      </div>
    </RouterLink>
  </article>
</template>


<style scoped>
/* =======================
   BASE
======================= */
.noticia-card {
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
}

.noticia-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.card-link {
  text-decoration: none;
  color: #333;
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* =======================
   IMAGEM
======================= */
.capa,
.sem-capa {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.sem-capa {
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

/* =======================
   CONTEÚDO
======================= */
.conteudo {
  padding: 16px;
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
}

.meta {
  font-size: 0.8rem;
  color: #777;
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid #f5f5f5;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.tag {
  font-size: 0.7rem;
  background: #f0f0f0;
  color: #666;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 500;
}

/* =======================
   VARIANT: CAROUSEL
======================= */
.noticia-card.carousel {
  height: auto;            /* 🔥 NÃO ESTICA */
}

.noticia-card.carousel .capa,
.noticia-card.carousel .sem-capa {
  height: 180px;
}

.noticia-card.carousel .subtitulo {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

</style>
