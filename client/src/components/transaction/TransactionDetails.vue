<!-- src/components/transaction/TransactionDetails.vue -->
<template>
  <glass-card>
    <q-card-section>
      <div class="text-h6">Detalhes da Transação</div>
      <div class="text-subtitle2">{{ transaction.txid }}</div>
    </q-card-section>

    <q-separator dark inset />

    <q-card-section>
      <div class="row q-col-gutter-md">
        <!-- Status -->
        <div class="col-12 col-md-6">
          <q-badge :color="transaction.isConfirmed ? 'positive' : 'warning'">
            {{ transaction.isConfirmed ? 'Confirmada' : 'Não Confirmada' }}
          </q-badge>
          <div v-if="transaction.isConfirmed" class="q-mt-sm">
            Confirmações: {{ transaction.confirmations }}
          </div>
        </div>

        <!-- Tempo -->
        <div class="col-12 col-md-6">
          <div class="text-caption">Data/Hora</div>
          <div>{{ transaction.formattedTime }}</div>
        </div>

        <!-- Tamanho -->
        <div class="col-12 col-md-4">
          <div class="text-caption">Tamanho</div>
          <div>{{ transaction.formattedSize }}</div>
        </div>

        <!-- Peso -->
        <div class="col-12 col-md-4">
          <div class="text-caption">Peso</div>
          <div>{{ transaction.formattedWeight }}</div>
        </div>

        <!-- Taxa -->
        <div class="col-12 col-md-4">
          <div class="text-caption">Taxa</div>
          <div>{{ transaction.formattedFee }}</div>
          <div class="text-caption">{{ transaction.formattedFeeRate }}</div>
        </div>
      </div>

      <!-- Entradas -->
      <div class="q-mt-lg">
        <div class="text-subtitle2">Entradas</div>
        <q-list dark bordered separator>
          <q-item v-for="input in transaction.inputs" :key="input.txid">
            <q-item-section>
              <q-item-label>{{ input.txid }}</q-item-label>
              <q-item-label caption>
                {{ input.formattedValue }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- Saídas -->
      <div class="q-mt-md">
        <div class="text-subtitle2">Saídas</div>
        <q-list dark bordered separator>
          <q-item v-for="output in transaction.outputs" :key="output.n">
            <q-item-section>
              <q-item-label>{{ output.scriptPubKey }}</q-item-label>
              <q-item-label caption>
                {{ output.formattedValue }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-card-section>
  </glass-card>
</template>

<script setup lang="ts">
import type { Transaction } from 'src/models/Transaction'

defineProps<{
  transaction: Transaction
}>()
</script>