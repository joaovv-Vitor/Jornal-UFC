<script setup lang="ts">
import type { RoleEnum, RoleOption } from '../types/roles'

const props = defineProps<{
  modelValue: RoleEnum;
  options: RoleOption[];
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: RoleEnum): void;
}>();

function updateRole(event: Event) {
  const target = event.target as HTMLSelectElement;
  emit('update:modelValue', target.value as RoleEnum);
}
</script>

<template>
  <div class="user-type-selector">
    <label>Tipo de Usuário</label>

    <select :value="modelValue" @change="updateRole">
      <option 
        v-for="opt in options" 
        :key="opt.value" 
        :value="opt.value"
      >
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.user-type-selector {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

select {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #444;
}
</style>
