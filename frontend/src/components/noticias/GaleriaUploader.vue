<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'

const props = defineProps<{
  initialUrls?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:files', payload: File[]): void
}>()

const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement | null>(null)

// 💡 Gerenciamento de URLs para evitar Memory Leak
const objectUrls = ref<string[]>([])

const previewUrls = computed(() => {
  const existingUrls = props.initialUrls || []
  
  // Revoga URLs antigas antes de criar novas para não travar o navegador
  objectUrls.value.forEach(url => URL.revokeObjectURL(url))
  objectUrls.value = files.value.map(file => URL.createObjectURL(file))
  
  return [...existingUrls, ...objectUrls.value]
})

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const newFiles = input.files
  
  if (newFiles) {
    // Adiciona sem sobrescrever os que já foram selecionados
    files.value = [...files.value, ...Array.from(newFiles)]
    emit('update:files', files.value)
  }
}

function removeFile(index: number) {
  const existingCount = props.initialUrls?.length || 0
  
  if (index < existingCount) {
    // 💡 Lógica para imagens que JÁ ESTÃO no servidor
    // Para a Sprint 2, você pode apenas emitir um alerta ou ignorar, 
    // pois a exclusão de fotos antigas exigiria uma rota de DELETE específica.
    alert("Para remover fotos já salvas, use a tela de edição.")
  } else {
    // 💡 Remove apenas os arquivos novos (locais)
    const relativeIndex = index - existingCount
    files.value.splice(relativeIndex, 1)
    emit('update:files', files.value)
  }
}

onBeforeUnmount(() => {
  objectUrls.value.forEach(url => URL.revokeObjectURL(url))
})
</script>

<template>
  <div class="galeria-uploader">
    <label class="label">Galeria de Imagens (Opcional)</label>

    <div class="previews-container">
      <div v-for="(url, index) in previewUrls" :key="url" class="preview-item">
        <img :src="url" alt="Imagem da Galeria" class="preview-img" />
        <button type="button" class="remove-btn" @click="removeFile(index)">
          &times;
        </button>
      </div>
      
      <button type="button" class="add-button" @click="fileInput?.click()">
        + Adicionar Fotos ({{ files.length }})
      </button>
    </div>

    <input 
      ref="fileInput"
      type="file" 
      accept="image/*" 
      multiple
      @change="onFileChange" 
      class="file-input"
    />
  </div>
</template>

<style scoped>
/* Seus estilos originais permanecem os mesmos */
.galeria-uploader { display: flex; flex-direction: column; gap: 10px; }
.label { font-weight: 600; color: #333; }
.previews-container { display: flex; flex-wrap: wrap; gap: 10px; padding: 10px 0; }
.preview-item { width: 100px; height: 100px; border-radius: 6px; overflow: hidden; position: relative; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
.preview-img { width: 100%; height: 100%; object-fit: cover; }
.remove-btn { position: absolute; top: 2px; right: 2px; background: rgba(156, 6, 13, 0.8); color: white; border: none; border-radius: 50%; width: 20px; height: 20px; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.file-input { display: none; }
.add-button { padding: 10px; border: 2px dashed #9c060d; border-radius: 6px; background: none; color: #9c060d; cursor: pointer; font-size: 14px; height: 100px; align-self: flex-start; }
</style>