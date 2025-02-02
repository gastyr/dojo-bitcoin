import { boot } from 'quasar/wrappers'

export default boot(({ app }) => {
  // Força o tema escuro
  app.config.globalProperties.$q.dark.set(true)
})