<template>
  <q-toolbar class="app-toolbar">
    <!-- Logo e Título -->
    <div class="app-toolbar__brand">
      <q-btn
        flat
        round
        dense
        class="app-toolbar__logo q-mr-sm"
      >
        <q-icon name="currency_bitcoin" size="32px" class="text-orange-400" />
      </q-btn>
      
      <q-toolbar-title class="app-toolbar__title" shrink>
        Hash Heroes Bitcoin Explorer
        <q-chip
          v-if="networkInfo?.isTestnet"
          dense
          class="app-toolbar__network-badge q-ml-sm"
        >
          {{ networkInfo.networkName }}
        </q-chip>
      </q-toolbar-title>
    </div>

    <!-- Status da Rede -->
    <network-stats class="app-toolbar__stats" />
  </q-toolbar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNetworkStore } from 'stores/network'
import NetworkStats from './NetworkStats.vue'

const networkStore = useNetworkStore()
const networkInfo = computed(() => networkStore.networkInfo)
</script>

<style lang="scss" scoped>
.app-toolbar {
  background: linear-gradient(
    90deg,
    rgba(23, 32, 46, 0.8) 0%,
    $grey-10 100%
  );
  backdrop-filter: blur(10px);
  // border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  height: 72px;  // Toolbar mais alto
  padding: 0 24px;
  
  // Sombra sofisticada
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);

  &__brand {
    color: white;
    display: flex;
    align-items: center;
    flex: 1;
    min-width: 0;
  }

  &__logo {
    .q-icon {
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
      transition: transform 0.3s ease;
    }

    &:hover .q-icon {
      transform: rotate(-15deg);
    }
  }

  &__title {
    white-space: nowrap;  // Evita quebra de linha
    overflow: visible !important;  // Sobrescreve o comportamento padrão do Quasar
    text-overflow: unset !important;  // Sobrescreve o comportamento padrão do Quasar
    flex-shrink: 0;  // Evita que o título seja comprimido
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    // Animação de entrada
    animation: slide-down 0.5s ease-out;
  }

  &__network-badge {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 4px 8px;
    
    // Efeito de brilho
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    
    // Animação de entrada
    animation: scale-in 0.3s ease-out;
  }

  &__stats {
    margin-left: 24px;  // Empurra para a direita
    padding-left: 24px;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }
}

// Animações
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

// Responsividade
@media (max-width: 599px) {
  .app-toolbar {
    padding: 0 16px;
    height: 64px;

    &__title {
      font-size: 1.25rem;
    }

    &__stats {
      padding-left: 16px;
    }
  }
}
</style>