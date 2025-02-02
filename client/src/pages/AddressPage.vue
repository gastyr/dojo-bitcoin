<template>
  <q-page class="q-pa-lg">
    <div class="max-width-1024 q-mx-auto">
      <!-- Search Component -->
      <address-search
        v-model="userInput"
        :loading="loading"
        @search="searchAddress"
        class="q-mb-lg"
      />
      <!-- Content -->
      <div v-if="address">
        <address-overview :balance-data="address"/>
        <unspent-outputs-table
          class="q-mt-lg"
          :outputs="address.unspentOutputs"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import AddressOverview from 'src/components/address/AddressOverview.vue'
import UnspentOutputsTable from 'src/components/address/UnspentOutputsTable.vue'
import AddressSearch from 'src/components/address/AddressSearch.vue'
import { addressService } from 'src/services/address'
import type { Address } from 'src/models/Address'

const userInput = ref('')
const $q = useQuasar()
const loading = ref(false)
const address = ref<Address | null>(null)

async function searchAddress() {
  try {
    loading.value = true
    address.value = await addressService.getAddress(userInput.value)
    
    $q.notify({
      type: 'positive',
      message: 'Transação encontrada!',
      position: 'bottom',
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error instanceof Error ? error.message : 'Erro ao buscar carteira',
      position: 'bottom',
    })
    address.value = null
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.max-width-1024 {
  max-width: 1024px;
}
</style>