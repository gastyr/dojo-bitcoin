<template>
  <glass-card>
    <q-card-section>
      <div class="text-h6 q-mb-sm">Consultar Saldo</div>
        <q-form @submit.prevent="handleSearch" class="row q-gutter-y-md">
          <div class="col-12">
          <q-input
            ref="inputRef"
            v-model="localValue"
            filled
            placeholder="Endereço Bitcoin (ex: bc1...)"
            :rules="addressRules"
            lazy-rules="ondemand"
          >
            <template v-slot:prepend>
              <q-icon name="search"/>
            </template>
            <template v-slot:append>
              <q-btn
                round
                flat
                dense
                icon="travel_explore"
                type="submit"
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

const addressRules = [
  (val: string) => !!val || 'Campo obrigatório',
  (val: string) => /^bcrt1[a-z0-9]{39,59}$/.test(val) || 'Endereço inválido'
]

function handleSearch() {
  if (inputRef.value.validate()) {
      emit('search')
    }
  }

</script>

<style lang="scss" scoped>
.q-btn {
  transition: transform 0.3s ease;
  
  &:hover {
    transform: rotate(20deg);
  }
}
</style>