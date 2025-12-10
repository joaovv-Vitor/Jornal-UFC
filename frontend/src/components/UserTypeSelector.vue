<script setup lang="ts">
const props = defineProps<{
  label: string
  modelValue: string
  options: string[]
}>()

const emit = defineEmits(['update:modelValue'])

function updateValue(event: Event) {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="input-field">
    <label>{{ label }}</label>

    <select :value="modelValue" @change="updateValue">
      <option disabled value="">Selecione...</option>
      <option
        v-for="opt in options"
        :key="opt"
        :value="opt"
      >
        {{ opt }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.input-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-family: Arial, Helvetica, sans-serif;
}

.input-field select {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #444;
  font-size: 15px;
  background: none;
}

.input-field label {
  font-weight: bold;
}
</style>
