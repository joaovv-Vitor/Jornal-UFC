<script setup lang="ts">
import { ref, watch } from 'vue'

/**
 * Propriedades
 * - initialFile: Se estiver editando, pode ser o URL da imagem existente.
 */
const props = defineProps<{
  initialUrl?: string
}>()

/**
 * Emits
 * - update:file: Emite o arquivo File (ou null) selecionado.
 */
const emit = defineEmits<{
  (e: 'update:file', payload: File | null): void
}>()

// Estado interno
const fileInput = ref<HTMLInputElement | null>(null)
const previewUrl = ref<string | null>(props.initialUrl || null)

// Manipula a seleção de arquivo
function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  if (file) {
    // 1. Cria a URL de pré-visualização no navegador
    previewUrl.value = URL.createObjectURL(file)
    // 2. Emite o arquivo para o formulário pai
    emit('update:file', file)
  } else {
    // 3. Limpa se não houver arquivo
    previewUrl.value = props.initialUrl || null
    emit('update:file', null)
  }
}

// Limpa o arquivo (útil para edição)
function clearFile() {
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  previewUrl.value = props.initialUrl || null
  emit('update:file', null)
}

// Limpa a URL de objeto quando o componente for destruído (boa prática)
watch(previewUrl, (newUrl, oldUrl) => {
    if (oldUrl && oldUrl !== props.initialUrl) {
        URL.revokeObjectURL(oldUrl);
    }
}, { immediate: true })

</script>

<template>
  <div class="capa-uploader">
    <label class="label">Imagem de Capa *</label>

    <div class="preview-area" :class="{ 'has-image': previewUrl }">
      <img v-if="previewUrl" :src="previewUrl" alt="Prévia da Capa" class="preview-img" />
      <span v-else class="placeholder-text">Selecione uma imagem (JPG, PNG ou WEBP)</span>
    </div>

    <input 
      ref="fileInput"
      type="file" 
      accept="image/jpeg, image/png, image/webp" 
      @change="onFileChange" 
      class="file-input"
    />

    <button v-if="!previewUrl" type="button" class="upload-button" @click="fileInput?.click()">
      Escolher Arquivo
    </button>
    
    <button v-else type="button" class="clear-button" @click="clearFile()">
      Remover Imagem
    </button>
  </div>
</template>

<style scoped>
.capa-uploader {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.label {
  font-weight: 600;
  color: #333;
}

.preview-area {
  width: 100%;
  height: 200px;
  border: 2px dashed #ccc;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  background-color: #f9f9f9;
}

.preview-area.has-image {
  border: none;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-text {
  color: #999;
  font-style: italic;
}

/* Oculta o input real e usa o botão customizado */
.file-input {
  display: none;
}

.upload-button, .clear-button {
  padding: 8px 15px;
  border: 1px solid #9c060d;
  border-radius: 6px;
  background-color: #9c060d;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 14px;
}

.clear-button {
  background-color: #ccc;
  border-color: #999;
  color: #333;
}
</style>