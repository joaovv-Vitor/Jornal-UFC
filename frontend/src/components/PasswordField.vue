<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  label: string
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits(['update:modelValue'])

const isVisible = ref(false)

function updateValue(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="input-field">
    <label>{{ label }}</label>

    <div class="password-wrapper">
      <input
        :type="isVisible ? 'text' : 'password'"
        :placeholder="placeholder"
        :value="modelValue"
        @input="updateValue"
      />

      <button
        type="button"
        class="toggle-btn"
        @click="isVisible = !isVisible"
      >
        {{ isVisible ? '👁️' : '👁️‍🗨️' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.input-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: none;
  font-family: Arial, Helvetica, sans-serif;
}

.password-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #444;
  border-radius: 6px;
  padding-right: 6px;
  background: none;
}

.password-wrapper input {
  flex: 1;
  padding: 10px;
  border: none;
  font-size: 15px;
  background: none;
}

.password-wrapper input:focus {
  outline: none;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.input-field label {
  font-weight: bold;
  background: none;
}
</style>
