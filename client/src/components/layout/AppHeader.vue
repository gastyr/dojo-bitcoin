<template>
  <q-header class="bg-transparent">
    <app-toolbar/>
    <app-navigation/>
    <div class="separator"/>
  </q-header>
</template>

<script setup lang="ts">
import AppToolbar from './AppToolbar.vue'
import AppNavigation from './AppNavigation.vue'
</script>

<style lang="scss" scoped>
.separator {
  width: 90%;
  margin: auto;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);  /* Linha discreta */
}
</style>