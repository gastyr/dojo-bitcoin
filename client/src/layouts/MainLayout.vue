<template>
  <q-layout view="hHh lpR fFf" class="main-layout">
    
    <div class="background-gradient" />
    <div class="background-pattern" />
    <app-header class="navigation-container"/>
    <q-page-container>
      <router-view v-slot="{ Component }">
          <component :is="Component" />
      </router-view>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useNetworkStore } from 'stores/network'
import AppHeader from 'components/layout/AppHeader.vue'

const networkStore = useNetworkStore()

onMounted(() => {
  networkStore.startNetworkMonitor()
})
</script>


<style lang="scss">
.main-layout {
  min-height: 100vh;
  position: relative;
  overflow: hidden;

  .background-gradient {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(23, 32, 46, 0.95) 0%,
      rgba(26, 42, 76, 0.95) 50%,
      rgba(32, 55, 96, 0.95) 100%
    );
    z-index: -2;
  }

  .background-pattern {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.05) 1%, transparent 1%),
      radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.05) 1%, transparent 1%);
    background-size: 100px 100px;
    opacity: 0.5;
    z-index: -1;
  }

  .content-container {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 1440px;
    margin: 0 auto;
    width: 100%;
  }
}

// Animação sutil para transições de rota
.q-page {
  transition: all 0.3s ease;
  
  &-enter-active, &-leave-active {
    transition: opacity 0.3s ease;
  }
  
  &-enter-from, &-leave-to {
    opacity: 0;
  }
}
</style>