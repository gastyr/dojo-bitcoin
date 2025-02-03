// src/boot/axios.ts
import { boot } from 'quasar/wrappers'
import axios from 'axios'
import type { AxiosInstance } from 'axios'


declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance
  }
}

// const baseURL = 'http://136.248.90.25:8000'
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
// const baseURL = window.__CONFIG__.VITE_API_BASE_URL || 'http://localhost:8000';


const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
})

// Interceptor para debug
api.interceptors.request.use(config => {
  console.log('Request:', config.method?.toUpperCase(), config.url)
  console.log(baseURL)
  return config
})

api.interceptors.response.use(
  response => {
    console.log('Response:', response.status, response.config.url)
    return response
  },
  error => {
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    })
    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }