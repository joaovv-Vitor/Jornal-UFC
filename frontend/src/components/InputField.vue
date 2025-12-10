<script setup lang="ts">
const props = defineProps<{
  label: string
  modelValue: string
  type?: string
  placeholder?: string
}>()

const emit = defineEmits(['update:modelValue'])

function updateValue(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="input-field">
    <label>{{ label }}</label>
    <input
      :type="type ?? 'text'"
      :placeholder="placeholder"
      :value="modelValue"
      @input="updateValue"
    />
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

.input-field input {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #444;
  font-size: 15px;
  background: none;
}

.input-field label {
  font-weight: bold;
  background: none;
}
</style>
