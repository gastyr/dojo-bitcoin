<template>
  <div class="col-12 col-md-8 offset-md-2">
    <glass-card>
      <q-card-section>
        <div class="text-h6">Detalhes do Bloco #{{ block.height }}</div>
      </q-card-section>

      <q-separator dark />

      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label caption>Hash</q-item-label>
                  <q-item-label class="text-orange-400">{{ block.hash }}</q-item-label>
                </q-item-section>
              </q-item>
              
              <q-item>
                <q-item-section>
                  <q-item-label caption>Data</q-item-label>
                  <q-item-label>{{ block.formattedTime }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section>
                  <q-item-label caption>Nonce</q-item-label>
                  <q-item-label>{{ block.nonce }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>

          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label caption>Dificuldade</q-item-label>
                  <q-item-label>{{ block.difficulty }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section>
                  <q-item-label caption>Tamanho / Peso</q-item-label>
                  <q-item-label>{{ block.size }} bytes / {{ block.weight }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section>
                  <q-item-label caption>Merkle Root</q-item-label>
                  <q-item-label class="text-orange-400">{{ block.merkleRoot }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </q-card-section>

      <block-transactions 
        :transactions="block.transactions"
        :num-transactions="block.numTransactions"
      />
    </glass-card>
  </div>
</template>

<script setup lang="ts">
import type { Block } from 'src/models/Block'
import BlockTransactions from './BlockTransactions.vue'

defineProps<{
  block: Block
}>()
</script>