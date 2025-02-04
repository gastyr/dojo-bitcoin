<template>
  <div class="col-12 col-md-6 offset-md-3">
    <glass-card>
      <q-card-section>
        <div class="text-h6 q-mb-sm">Explorar Bloco</div>
        <q-form @submit.prevent="handleSearch" class="row q-col-gutter-md">
          <div class="col-12">
            <q-input
              v-model.number="blockNumber"
              label="Número do Bloco"
              type="number"
              :rules="blockRules"
              filled
              dark
              lazy-rules
            >
              <template v-slot:prepend>
                <q-icon name="layers" />
              </template>
              <template v-slot:append>
                <q-btn
                  flat
                  round
                  dense
                  icon="search"
                  type="submit"
                  @click.prevent="handleSearch"
                  :loading="loading"
                />
              </template>
            </q-input>
          </div>
        </q-form>
      </q-card-section>
    </glass-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { blockService } from 'src/services/block'
import type { Block } from 'src/models/Block'

const emit = defineEmits<{
  (e: 'block-found', block: Block | null): void
}>()

const $q = useQuasar()
const blockNumber = ref<number | null>(null)
const loading = ref(false)

const blockRules = [
  (val: number | null) => val !== null || 'Campo obrigatório',
  (val: number) => val >= 0 || 'Número inválido'
]

async function handleSearch() {
  if (blockNumber.value === null) return

  loading.value = true
  try {
    const block = await blockService.getBlock(blockNumber.value)
    emit('block-found', block)
    $q.notify({
      type: 'positive',
      message: 'Bloco encontrado!',
      position: 'bottom'
    })
  } catch (error) {
    console.error('Erro ao buscar bloco:', error)
    const message = error instanceof Error ? error.message : 'Erro ao buscar bloco'
    $q.notify({
      type: 'negative',
      message,
      position: 'bottom'
    })
    emit('block-found', null)
  } finally {
    loading.value = false
  }
}
</script>