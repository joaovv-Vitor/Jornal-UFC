<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import CapaUploader from './CapaUploader.vue'
import GaleriaUploader from './GaleriaUploader.vue'

const props = defineProps<{
  initialData?: {
    titulo?: string
    subtitulo?: string
    conteudo?: string
    tags?: string[]
    categoria_id?: number | null
    imagem_capa?: string 
  }
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'submit', payload: FormData): void
}>()

const form = reactive({
  titulo: props.initialData?.titulo ?? '',
  subtitulo: props.initialData?.subtitulo ?? '',
  conteudo: props.initialData?.conteudo ?? '',
  tags: props.initialData?.tags?.join(', ') ?? '',
  categoria_id: props.initialData?.categoria_id ?? null
})

// 💡 Definindo tipos explicitamente para evitar erro de 'any'
const imagemCapa = ref<File | null>(null)
const galeria = ref<File[]>([])
const errorMessage = ref('')

const isValid = computed(() => {
  return form.titulo.trim() && form.conteudo.trim()
})

// Altere as chamadas dos componentes no template para incluir os tipos
const handleCapaUpdate = (file: File | null) => { 
  imagemCapa.value = file 
}

const handleGaleriaUpdate = (files: File[]) => { 
  galeria.value = files 
}

function submit() {
  errorMessage.value = ''

  if (!isValid.value) {
    errorMessage.value = 'Título e conteúdo são obrigatórios.'
    return
  }

  const formData = new FormData()
  formData.append('titulo', form.titulo)
  formData.append('conteudo', form.conteudo)

  if (form.subtitulo) formData.append('subtitulo', form.subtitulo)
  if (form.tags) formData.append('tags', form.tags)
  if (form.categoria_id) formData.append('categoria_id', String(form.categoria_id))

  if (imagemCapa.value) {
    formData.append('imagem_capa', imagemCapa.value)
  }

  // 💡 Loop correto para o FastAPI receber múltiplos arquivos
  galeria.value.forEach((file) => {
    formData.append('galeria', file)
  })

  emit('submit', formData)
}
</script>

<template>
  <form class="noticia-form" @submit.prevent="submit">
    <div class="field">
      <label>Título *</label>
      <input v-model="form.titulo" type="text" placeholder="Digite o título" />
    </div>

    <div class="field">
      <label>Subtítulo</label>
      <input v-model="form.subtitulo" type="text" placeholder="Subtítulo opcional" />
    </div>

    <div class="field">
      <label>Conteúdo *</label>
      <textarea v-model="form.conteudo" rows="8" placeholder="Escreva o conteúdo aqui..." />
    </div>

    <div class="field">
      <label>Tags</label>
      <input v-model="form.tags" type="text" placeholder="Ex: ufc, tecnologia, educação" />
    </div>

    <div class="field">
      <CapaUploader 
        :initial-url="props.initialData?.imagem_capa" 
        @update:file="handleCapaUpdate" 
      />
    </div>

    <div class="field">
      <GaleriaUploader @update:files="handleGaleriaUpdate" />
    </div>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Salvando...' : 'Salvar Notícia' }}
    </button>
  </form>
</template>

<style scoped>
.noticia-form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
input, textarea { padding: 10px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; }
textarea { resize: vertical; }
button {
  margin-top: 10px; padding: 12px; border: none; border-radius: 6px;
  background-color: #9c060d; color: white; font-size: 16px; font-weight: bold; cursor: pointer;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error-message {
  color: #d93025; background-color: #ffe8e8; padding: 8px; border-radius: 4px;
  text-align: center; font-size: 14px; font-weight: bold;
}
</style>