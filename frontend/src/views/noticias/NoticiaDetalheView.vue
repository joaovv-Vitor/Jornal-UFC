<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { buscarNoticia } from '../../services/noticias.api'

const route = useRoute()
const router = useRouter()
const noticia = ref<any>(null)
const loading = ref(true)

const getImageUrl = (path: string | undefined | null) => {
  if (!path) return ''
  return path.startsWith('http') ? path : `http://localhost:8000${path}`
}

onMounted(async () => {
  try {
    const slug = route.params.slug as string
    const response = await buscarNoticia(slug)
    noticia.value = response.data
  } catch (e) {
    console.error(e)
    router.push('/')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="detalhe-wrapper">
    <div v-if="loading" class="msg">Carregando...</div>
    <article v-else-if="noticia" class="noticia-body">
      <button @click="router.back()">← Voltar</button>
      
      <img v-if="noticia.imagem_capa" :src="getImageUrl(noticia.imagem_capa)" class="capa">
      
      <h1>{{ noticia.titulo }}</h1>
      <p class="sub">{{ noticia.subtitulo }}</p>
      
      <div class="content" v-html="noticia.conteudo"></div>

      <div v-if="noticia.imagens_galeria?.length" class="galeria">
        <img v-for="img in noticia.imagens_galeria" :key="img.id" :src="getImageUrl(img.caminho)">
      </div>
    </article>
  </div>
</template>

<style scoped>
/* Garante que o fundo aqui seja claro para você ler o texto */
.detalhe-wrapper { background: #f4f4f4; min-height: 100vh; padding: 20px; color: #333; }
.noticia-body { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
.capa { width: 100%; border-radius: 8px; margin: 20px 0; }
.content { line-height: 1.6; white-space: pre-wrap; }
.galeria { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; }
.galeria img { width: 100%; height: 150px; object-fit: cover; }
</style>