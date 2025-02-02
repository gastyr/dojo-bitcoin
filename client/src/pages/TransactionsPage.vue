<template>
  <q-page padding>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-8 offset-md-2">
        <!-- Componente de Busca -->
        <transaction-search
          v-model="txid"
          :loading="loading"
          @search="searchTransaction"
        />

        <!-- Componente de Detalhes ou Skeleton -->
        <template v-if="transaction">
          <transaction-details
            :transaction="transaction"
            class="q-mt-md"
          />
        </template>
        <transaction-skeleton v-else-if="loading" class="q-mt-md" />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { transactionService } from 'src/services/transaction'
import type { Transaction } from 'src/models/Transaction'
import TransactionSearch from 'components/transaction/TransactionSearch.vue'
import TransactionDetails from 'components/transaction/TransactionDetails.vue'
import TransactionSkeleton from 'components/transaction/TransactionSkeleton.vue'

const $q = useQuasar()
const txid = ref('')
const transaction = ref<Transaction | null>(null)
const loading = ref(false)

const passedTxid  = computed(() => history.state.txid || '');

onMounted(() => {
  if (passedTxid.value) {
    txid.value = passedTxid.value;
    searchTransaction()
  }
})

async function searchTransaction() {
  try {
    loading.value = true
    transaction.value = await transactionService.getTransaction(txid.value)
    $q.notify({
      type: 'positive',
      message: 'Transação encontrada!',
      position: 'bottom',
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error instanceof Error ? error.message : 'Erro ao buscar transação',
      position: 'bottom',
    })
    transaction.value = null
  } finally {
    loading.value = false
  }
}
</script>