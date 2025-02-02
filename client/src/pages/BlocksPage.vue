<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <block-search @block-found="onBlockFound" />
      <block-details v-if="block" :block="block" />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Block } from 'src/models/Block'
import BlockSearch from 'src/components/block/BlockSearch.vue'
import BlockDetails from 'src/components/block/BlockDetails.vue'

const block = ref<Block | null>(null)

function onBlockFound(foundBlock: Block | null) {
  block.value = foundBlock
}
</script>