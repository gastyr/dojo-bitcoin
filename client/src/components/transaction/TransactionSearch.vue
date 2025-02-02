<template>
  <glass-card>
    <q-card-section>
      <div class="text-h6 q-mb-sm">Explorar Transação</div>
      <q-form @submit.prevent="handleSearch" class="row q-col-gutter-md">
        <div class="col-12">
          <q-input
            ref="inputRef"
            v-model="localValue"
            filled
            label="ID da Transação (TXID)"
            :rules="txidRules"
            lazy-rules="ondemand"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
            <template v-slot:append>
              <q-btn
                flat
                round
                dense
                icon="send"
                :loading="props.loading"
                @click="handleSearch"
              />
            </template>
          </q-input>
        </div>
      </q-form>
    </q-card-section>
  </glass-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  modelValue: string
  loading?: boolean
}>()

const inputRef = ref()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'search': []
}>()

const localValue = computed({
  get: () => props.modelValue,
  set: (newValue) => emit('update:modelValue', newValue)
});

const txidRules = [
  (val: string) => !!val || 'Campo obrigatório',
  (val: string) => /^[0-9a-f]{64}$/i.test(val) || 'TXID inválido'
]

function handleSearch() {
  if (inputRef.value.validate()) {
      emit('search')
    }
  }
</script>