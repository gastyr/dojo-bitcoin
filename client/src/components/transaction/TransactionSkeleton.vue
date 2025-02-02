<template>
  <glass-card class="q-mt-md">
    <q-card-section>
      <div class="row items-center q-mb-md">
        <q-skeleton type="text" class="text-h6" width="200px" />
        <q-space />
        <q-skeleton type="QChip" width="100px" />
      </div>

      <div class="row q-col-gutter-md">
        <div class="col-12">
          <q-list dense>
            <q-item v-for="i in 4" :key="i">
              <q-item-section>
                <q-skeleton type="text" class="text-caption" width="80px" />
                <q-skeleton type="text" width="100%" />
              </q-item-section>
            </q-item>
          </q-list>
        </div>
      </div>

      <div class="row q-col-gutter-md q-mt-md">
        <div class="col-12 col-md-6" v-for="i in 2" :key="i">
          <glass-card>
            <q-card-section>
              <q-skeleton type="text" class="text-subtitle1" width="100px" />
              <q-list dense>
                <q-item v-for="j in 3" :key="j">
                  <q-item-section>
                    <q-skeleton type="text" width="100%" />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
          </glass-card>
        </div>
      </div>
    </q-card-section>
  </glass-card>
</template>

<script setup lang="ts">

</script>