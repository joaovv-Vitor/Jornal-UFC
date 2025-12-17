<script setup lang="ts">
import { ref, computed } from 'vue'

/**
 * Propriedades
 * - initialUrls: URLs das imagens existentes (em modo edição).
 */
const props = defineProps<{
  initialUrls?: string[]
}>()

/**
 * Emits
 * - update:files: Emite o array de arquivos File[] selecionados.
 */
const emit = defineEmits<{
  (e: 'update:files', payload: File[]): void
}>()

// Estado interno
const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement | null>(null)

const previewUrls = computed(() => {
    // 1. URLs existentes (para edição)
    const existingUrls = props.initialUrls || [];
    // 2. URLs de novos arquivos
    const newUrls = files.value.map(file => URL.createObjectURL(file));
    
    return [...existingUrls, ...newUrls];
});


function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const newFiles = input.files
  
  if (newFiles) {
    // 💡 IMPORTANTE: Adiciona novos arquivos à lista existente (se estiver em modo criação)
    files.value = [...files.value, ...Array.from(newFiles)]
  } else {
    // Se o input for resetado sem seleção, limpa
    files.value = []
  }
  
  emit('update:files', files.value)
}

function removeFile(index: number) {
    // Remove o arquivo da lista de arquivos
    files.value.splice(index, 1)
    emit('update:files', files.value)
}

// Limpar URLs de objeto ao desmontar (boa prática)
// Você também precisaria de uma lógica para remover os ObjectURLs se o componente for destruído
// Omitido por brevidade, mas deve ser considerado.
</script>

<template>
  <div class="galeria-uploader">
    <label class="label">Galeria de Imagens (Opcional)</label>

    <div class="previews-container">
        <div 
            v-for="(url, index) in previewUrls" 
            :key="url" 
            class="preview-item"
        >
            <img :src="url" alt="Imagem da Galeria" class="preview-img" />
            <button 
                type="button" 
                class="remove-btn" 
                @click="removeFile(index)"
            >
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
.galeria-uploader {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.label {
  font-weight: 600;
  color: #333;
}

.previews-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 0;
}

.preview-item {
  width: 100px;
  height: 100px;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  background: rgba(156, 6, 13, 0.8); /* Cor da marca UFC */
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.file-input {
  display: none;
}

.add-button {
    padding: 10px;
    border: 2px dashed #9c060d;
    border-radius: 6px;
    background: none;
    color: #9c060d;
    cursor: pointer;
    font-size: 14px;
    height: 100px;
    align-self: flex-start;
}
</style>