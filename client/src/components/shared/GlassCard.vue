<template>
  <q-card class="glass-card" :style="{ padding }">
    <slot />
  </q-card>
</template>

<script setup lang="ts">
defineProps({
  padding: {
    type: String,
    default: '16px',
  },
});
</script>

<style lang="scss" scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;

  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.2),
    0 2px 4px -1px rgba(0, 0, 0, 0.1);

  &:hover {
    transform: translateY(-3px);
    box-shadow: 
      0 8px 18px -3px rgba(0, 0, 0, 0.3),
      0 4px 6px -2px rgba(0, 0, 0, 0.2);
  }

}
</style>