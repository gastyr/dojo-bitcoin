// src/boot/components.ts
import { boot } from 'quasar/wrappers'
import GlassCard from 'components/shared/GlassCard.vue'

// Apenas componentes realmente globais/reutilizáveis
export default boot(({ app }) => {
  app.component('GlassCard', GlassCard)
})