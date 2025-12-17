<script setup lang="ts">

/**
 * Propriedades
 * - show: Controla a visibilidade do modal.
 * - title: Título da ação de confirmação.
 */
const props = defineProps<{
  show: boolean
  title: string
  message: string
  confirmText: string
}>()

/**
 * Emits
 * - confirm: Chamado quando o usuário confirma a ação.
 * - close: Chamado quando o usuário fecha/cancela.
 */
const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'close'): void
}>()

</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="modal-mask" @click.self="emit('close')">
        <div class="modal-wrapper">
          <div class="modal-container">
            
            <div class="modal-header">
              <h3>{{ title }}</h3>
              <button class="close-btn" @click="emit('close')">&times;</button>
            </div>

            <div class="modal-body">
              <p>{{ message }}</p>
            </div>

            <div class="modal-footer">
              <button class="cancel-button" @click="emit('close')">
                Cancelar
              </button>
              <button 
                class="confirm-button" 
                @click="emit('confirm')"
              >
                {{ confirmText }}
              </button>
            </div>

          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* Estilos Modais (Baseados em CSS simples) */
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  width: 400px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  margin-top: 0;
  color: #9c060d;
}

.modal-body {
  margin: 20px 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-button, .cancel-button {
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}

.confirm-button {
    background-color: #9c060d;
    color: white;
    border: none;
}

.cancel-button {
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
}

/* Transição */
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>