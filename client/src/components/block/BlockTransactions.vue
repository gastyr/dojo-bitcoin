<template>
  <q-card-section>
    <div class="text-h6 q-mb-md">
      Transações
      <q-chip color="orange" text-color="dark" class="q-ml-sm">
        {{ numTransactions }}
      </q-chip>
    </div>

    <q-list separator>
      <q-item
        v-for="tx in transactions"
        :key="tx.txid"
        clickable
        v-ripple
        @click="goToTransaction(tx.txid)"
      >
        <q-item-section>
          <q-item-label class="text-orange-400">{{ tx.txid }}</q-item-label>
          <q-item-label caption>
            <q-icon name="input" size="xs" /> {{ tx.inputCount }} inputs
            <q-icon name="output" size="xs" class="q-ml-sm" /> {{ tx.outputCount }} outputs
            <q-icon name="currency_bitcoin" size="xs" class="q-ml-sm" /> {{ tx.totalOutput }} BTC
          </q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-list>
  </q-card-section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps<{
  transactions: Array<{
    txid: string
    inputCount: number
    outputCount: number
    totalOutput: number
  }>
  numTransactions: number
}>()

function goToTransaction(txid: string) {
  router.push({
    path: '/transactions',
    state: { txid }
  });
}

</script>