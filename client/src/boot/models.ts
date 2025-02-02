// src/boot/models.ts
import { boot } from 'quasar/wrappers'
import * as Models from 'src/models'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $models: typeof Models
  }
}

export default boot(({ app }) => {
  // Injetando models como propriedade global
  app.config.globalProperties.$models = Models
})