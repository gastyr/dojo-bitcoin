<template>
  <q-tabs
    v-model="currentTab"
    dense
    class="app-navigation"
    active-color="white"
    indicator-color="transparent"
    align="center"
  >
    <q-route-tab
      v-for="route in routes"
      :key="route.name"
      :name="route.name"
      :to="route.route"
      :label="route.label"
      :icon="route.icon"
      class="app-navigation__tab"
      exact-active-class="q-tab--active"
    />
  </q-tabs>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

interface RouteMeta {
  tab?: string
  parent?: string
}

const route = useRoute()
const currentTab = ref<string>((route.meta as RouteMeta)?.tab || '')

const routes = [
  { 
    name: 'blocks', 
    route: '/blocks',
    label: 'Blocos', 
    icon: 'dashboard' 
  },
  { 
    name: 'transactions', 
    route: '/transactions', 
    label: 'Transações', 
    icon: 'swap_horiz' 
  },
  { 
    name: 'address', 
    route: '/address', 
    label: 'Endereços', 
    icon: 'account_balance_wallet' 
  },
]

watch(() => route.meta, (newMeta) => {
  const meta = newMeta as RouteMeta
  // Prefer parent meta when available for nested routes
  currentTab.value = meta.parent || meta.tab || ''
})

</script>


<style lang="scss" scoped>
.app-navigation {
  background: linear-gradient(
    135deg,
    #1e1631 0%,
    #131925 100%
  );
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 12px 24px;
  max-width: 60%;
  margin: 15px auto;

  &__tab {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    margin: 0 12px;
    padding: 6px 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    min-height: 64px;
    min-width: 120px;

    // Efeito hover
    &:hover {
      background: rgba(255, 255, 255, 0.08);
      transform: translateY(-1px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    // Tab ativo
    &.q-tab--active {
      background: rgba(78, 18, 36, 0.3);
      border: 1px solid;
      border-color: rgba(255, 165, 0, 0.3);
    }

    // Ícone
    :deep(.q-tab__icon) {
      font-size: 30px;
      transition: all 0.3s ease;
    }

    // Label
    :deep(.q-tab__label) {
      font-size: 0.9rem;
      font-weight: 500;
      margin-top: 4px;
      transition: color 0.3s ease;
    }
  }
}

// Animação de entrada para os tabs
.q-tab {
  animation: slide-down 0.3s ease-out;
  animation-fill-mode: both;
  @for $i from 1 through 4 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.2}s;
    }
  }
}



@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// Responsividade
@media (max-width: 599px) {
  .app-navigation {
    &__tab {
      padding: 0 12px;
      min-height: 48px;
      .q-tab__icon {
        font-size: 20px;
      }
      .q-tab__label {
        font-size: 0.8rem;
      }
    }
  }
}
</style>
