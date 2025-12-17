<script setup lang="ts">
import { reactive, ref, computed } from 'vue'

/**
 * Props
 * - initialData: usado no modo edição
 * - loading: desabilita o botão enquanto salva
 */
const props = defineProps<{
  initialData?: {
    titulo?: string
    subtitulo?: string
    conteudo?: string
    tags?: string[]
    categoria_id?: number | null
  }
  loading?: boolean
}>()

/**
 * Emits
 * - submit(FormData)
 */
const emit = defineEmits<{
  (e: 'submit', payload: FormData): void
}>()

// Estado do formulário
const form = reactive({
  titulo: props.initialData?.titulo ?? '',
  subtitulo: props.initialData?.subtitulo ?? '',
  conteudo: props.initialData?.conteudo ?? '',
  tags: props.initialData?.tags?.join(', ') ?? '',
  categoria_id: props.initialData?.categoria_id ?? null
})

// Arquivos
const imagemCapa = ref<File | null>(null)
const galeria = ref<File[]>([])

// Erros
const errorMessage = ref('')

// Validação mínima
const isValid = computed(() => {
  return form.titulo.trim() && form.conteudo.trim()
})

// Handlers
function onCapaChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] // 💡 Usamos Encaminhamento Opcional para obter File | undefined

  // 💡 MUDANÇA CRÍTICA: Se o arquivo existe (não é undefined), atribuímos. Caso contrário, é null.
  if (file) {
    imagemCapa.value = file
  } else {
    imagemCapa.value = null
  }
}

function onGaleriaChange(event: Event) {
  const input = event.target as HTMLInputElement
  const files = input.files
  
  // Garantir que files não é null
  if (files) {
    // Array.from lida bem com FileList, resultando em File[]
    galeria.value = Array.from(files) 
  } else {
    galeria.value = []
  }
}

// Submit
function submit() {
  errorMessage.value = ''

  if (!isValid.value) {
    errorMessage.value = 'Título e conteúdo são obrigatórios.'
    return
  }

  if (!imagemCapa.value && !props.initialData) {
    errorMessage.value = 'A imagem de capa é obrigatória.'
    return
  }

  const formData = new FormData()

  formData.append('titulo', form.titulo)
  formData.append('conteudo', form.conteudo)

  if (form.subtitulo) {
    formData.append('subtitulo', form.subtitulo)
  }

  if (form.tags) {
    formData.append('tags', form.tags)
  }

  if (form.categoria_id) {
    formData.append('categoria_id', String(form.categoria_id))
  }

  if (imagemCapa.value) {
    formData.append('imagem_capa', imagemCapa.value)
  }

  galeria.value.forEach((file) => {
    formData.append('galeria', file)
  })

  emit('submit', formData)
}
</script>

<template>
  <form class="noticia-form" @submit.prevent="submit">
    <h2>Notícia</h2>

    <div class="field">
      <label>Título *</label>
      <input v-model="form.titulo" type="text" placeholder="Título da notícia" />
    </div>

    <div class="field">
      <label>Subtítulo</label>
      <input v-model="form.subtitulo" type="text" placeholder="Subtítulo (opcional)" />
    </div>

    <div class="field">
      <label>Conteúdo *</label>
      <textarea
        v-model="form.conteudo"
        rows="8"
        placeholder="Conteúdo da notícia"
      />
    </div>

    <div class="field">
      <label>Tags</label>
      <input
        v-model="form.tags"
        type="text"
        placeholder="Ex: ufc, pesquisa, tecnologia"
      />
    </div>

    <div class="field">
      <label>Imagem de capa *</label>
      <input type="file" accept="image/*" @change="onCapaChange" />
    </div>

    <div class="field">
      <label>Galeria (opcional)</label>
      <input type="file" accept="image/*" multiple @change="onGaleriaChange" />
    </div>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Salvando...' : 'Salvar Notícia' }}
    </button>
  </form>
</template>

<style scoped>
.noticia-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input,
textarea {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

textarea {
  resize: vertical;
}

button {
  margin-top: 10px;
  padding: 12px;
  border: none;
  border-radius: 6px;
  background-color: #9c060d;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
</style>
