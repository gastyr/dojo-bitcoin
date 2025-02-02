<template>
  <glass-card>
  <q-card-section class="outputs-table q-pa-md">
    <div class="text-h6 q-mb-md">Unspent Transaction Outputs</div>
    
    <q-table
      :rows="props.outputs"
      :columns="columns"
      row-key="txid"
      :pagination="pagination"
      bordered
      :rows-per-page-options="[5, 10, 20]"
      rows-per-page-label="Registros por página"
      class="table"
    >
      <!-- Custom Header -->
      <template v-slot:header="headerProps">
        <q-tr :props="headerProps">
          <q-th
            v-for="col in headerProps.cols"
            :key="col.name"
            :props="headerProps"
            class="text-weight-medium text-center"
          >
          {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <!-- Custom Row Styling -->
      <template v-slot:body="bodyProps">
        <q-tr 
          :props="bodyProps"
          class="cursor-pointer"
          @click="goToTransaction(bodyProps.row.txid)"
        >
          <q-td v-for="col in bodyProps.cols" :key="col.name" class="text-center">
            <template v-if="col.name === 'txid'">
              <div class="row items-center justify-center">
                <span class="text-caption">{{ truncateTxId(bodyProps.row[col.field]) }}</span>
              </div>
            </template>
            
            <template v-else-if="col.name === 'confirmations'">
              <q-badge :color="getConfirmationColor(bodyProps.row[col.field])">
                {{ bodyProps.row[col.field] }} confirmações
              </q-badge>
            </template>

            <template v-else>
              {{ bodyProps.row[col.field] }}
            </template>
          </q-td>
        </q-tr>
      </template>

      <!-- Empty State -->
      <template v-slot:no-data>
        <div class="full-width row flex-center text-grey-3 q-pa-lg">
          Nenhum dado encontrado
        </div>
      </template>
    </q-table>
    </q-card-section>
  </glass-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import type { QTableColumn } from 'quasar'
import type { UnspentOutput } from 'src/models/Address'

const router = useRouter()
const $q = useQuasar()
const props = defineProps<{
  outputs: UnspentOutput[]
}>()

const columns = computed<QTableColumn[]>(() => [
  {
    name: 'txid',
    label: 'Transações TXID',
    field: 'txid',
    align: 'center',
    sortable: true
  },
  {
    name: 'vout',
    label: 'Índice',
    field: 'vout',
    align: 'center',
    sortable: true
  },
  {
    name: 'amount',
    label: 'Quantidade (BTC)',
    field: 'amount',
    align: 'center',
    sortable: true
  },
  {
    name: 'confirmations',
    label: 'Confirmações',
    field: 'confirmations',
    align: 'center',
    sortable: true
  }
])

const pagination = ref({
  descending: true,
  page: 1,
  rowsPerPage: 5
})

const truncateTxId = (txid: string) => {
  return $q.screen.lt.sm ? `${txid.slice(0, 8)}...${txid.slice(-6)}` : txid
}

const getConfirmationColor = (count: number) => {
  if (count > 100) return 'positive'
  if (count > 6) return 'warning'
  return 'negative'
}

function goToTransaction(txid: string) {
  router.push({
    path: '/transactions',
    state: { txid }
  });
}

</script>

<style lang="scss" scoped>
.outputs-table {
  .table {
    box-shadow: none
  }

  :deep(.q-table__card) {
    border: none;
    background: transparent;
  }
  
  :deep(.q-td) {
    padding: 16px;
  }

  // :deep(.q-tr > .q-td:not(:last-child)) {
  // border-right: 1px solid rgba(255, 255, 255, 0.3);
  // }
}
</style>