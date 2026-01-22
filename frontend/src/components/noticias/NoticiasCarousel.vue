<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { Noticia } from '../../types/noticias'
import NoticiaHighlight from './NoticiaHighlight.vue'

const props = defineProps<{
  noticias: Noticia[]
  titulo?: string
  autoplay?: boolean
  autoplayInterval?: number
}>()

const index = ref(0)

const noticiaAtual = computed<Noticia | null>(() => {
  return props.noticias[index.value] ?? null
})

const next = () => {
  index.value = (index.value + 1) % props.noticias.length
}

const prev = () => {
  index.value =
    (index.value - 1 + props.noticias.length) % props.noticias.length
}

let timer: number | undefined

onMounted(() => {
  if (props.autoplay) {
    timer = window.setInterval(
      next,
      props.autoplayInterval || 5000
    )
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <section v-if="noticias.length" class="carousel">
    <h2 v-if="titulo" class="carousel-title">{{ titulo }}</h2>

    <div class="carousel-wrapper">
      <button class="nav left" @click="prev">‹</button>

      <NoticiaHighlight
      v-if="noticiaAtual" 
      :noticia="noticiaAtual"
      />

      <button class="nav right" @click="next">›</button>
    </div>

    <div class="dots">
      <span
        v-for="(_, i) in noticias"
        :key="i"
        :class="{ active: i === index }"
        @click="index = i"
      />
    </div>
  </section>
</template>

<style scoped>
.carousel {
  margin: 40px 20px;
}

.carousel-title {
  font-size: 1.6rem;
  margin-bottom: 16px;
  color: #023b79;
}

.carousel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #0d6efd;
  color: white;
  border: none;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  font-size: 1.6rem;
  cursor: pointer;
  z-index: 2;
}

.nav.left { left: 12px; transition: all 0.3s ease; }
.nav.right { right: 12px; transition: all 0.3s ease; }

.nav.left:hover, .nav.right:hover {
  background: #0b5ed7;
}

.dots {
  display: flex;
  justify-content: center;
  margin-top: 12px;
  gap: 8px;
}

.dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
  cursor: pointer;
}

.dots span.active {
  background: #0d6efd;
}
</style>
