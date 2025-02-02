import type { RouteRecordRaw } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    tab?: string
  }
}

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/blocks'
      },
      {
        path: '/blocks',
        name: 'blocks',
        component: () => import('pages/BlocksPage.vue'),
        meta: { tab: 'blocks' }
      },
      {
        path: '/transactions',
        name: 'transactions',
        component: () => import('pages/TransactionsPage.vue'),
        meta: { tab: 'transactions'},
        // children: [
        //   {
        //     path: ':txid',
        //     name: 'transaction-details',
        //     component: () => import('pages/TransactionsPage.vue'),
        //   }
        // ]
      },
      {
        path: '/address',
        name: 'address',
        component: () => import('pages/AddressPage.vue'),
        meta: { tab: 'address' }
      },
    ],
  },

  // Página de erro 404
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]