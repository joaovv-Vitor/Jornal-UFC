<script setup lang="ts">
defineProps<{
  to?: string
  label?: string
}>()
</script>

<template>
  <router-link :to="to || '/login'" class="back-button">
    <span class="arrow">←</span>
    {{ label || 'Voltar' }}
  </router-link>
</template>

<style scoped>
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #000000;
  text-decoration: none;
  font-size: 18x;
  font-weight: 600;
  transition: color 0.2s ease, transform 0.2s ease;
  cursor: pointer;
  margin-top: 10px;
  padding: 20px;
}

.back-button:hover {
  color: #ff000d;
  transform: translateX(-4px); /* Efeito visual de "voltar" */
}
</style>
