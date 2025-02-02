<template>
  <glass-card>
    <q-card-section class="q-pa-md">
      <div v-if="balanceData" class="row items-center q-col-gutter-lg">
        <!-- Address Info -->
        <div class="col-12 col-md-8">
          <div class="text-h6 text-weight-medium">{{ balanceData.address }}</div>
          <div class="text-caption text-grey-4 q-mt-xs">
            Network:
            <q-badge :color="networkBadgeColor" class="q-ml-sm">
              {{ balanceData.network }}
            </q-badge>
          </div>
        </div>
        <!-- Balance Info -->
        <div class="col-12 col-md-4">
          <div class="text-right">
            <div class="text-h5 text-primary text-weight-bold">
              {{ balanceData.balance }} BTC
            </div>
            <div class="text-caption text-grey-4 q-mt-xs">
              {{ balanceData.unspentCount }} Unspent Outputs
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-grey-4 q-pa-md text-center">
        No address data available
      </div>
    </q-card-section>
  </glass-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Address } from 'src/models/Address'

const props = defineProps<{
  balanceData: Address | null
}>()

const networkBadgeColor = computed(() => {
  if (!props.balanceData) return 'grey'
  return props.balanceData.network === 'regtest' ? 'teal' : 'blue'
})
</script>