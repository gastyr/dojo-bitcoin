// src/stores/network.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Network } from 'src/models/Network'
import { networkService } from 'src/services/network'

export const useNetworkStore = defineStore('network', () => {
  const networkInfo = ref<Network | null>(null)

  async function updateNetworkInfo() {
    try {
      const data = await networkService.getNetworkInfo()
      networkInfo.value = data
    } catch (error) {
      console.error('Erro ao atualizar informações da rede:', error)
    }
  }

  function startNetworkMonitor() {
    updateNetworkInfo()
    // Atualiza a cada 30 segundos
    setInterval(updateNetworkInfo, 30000)
  }

  return {
    networkInfo,
    updateNetworkInfo,
    startNetworkMonitor
  }
})