<template>
  <div class="row q-gutter-x-md items-center">
    <!-- Último Bloco -->
    <div class="column items-end">
      <div class="text-caption text-grey-4">Último Bloco</div>
      <div class="text-weight-medium">{{ networkInfo?.lastBlock || '---' }}</div>
    </div>
    
    <q-separator vertical dark />
    
    <!-- Tamanho do Mempool -->
    <div class="column items-end">
      <div class="text-caption text-grey-4">Mempool</div>
      <div class="text-weight-medium">
        {{ networkInfo?.mempoolSize || '---' }} tx</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNetworkStore } from 'stores/network'
import type { Network } from 'src/models/Network'

const networkStore = useNetworkStore()
const networkInfo = computed<Network | null>(() => networkStore.networkInfo)
</script>