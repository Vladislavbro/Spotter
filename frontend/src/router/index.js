import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: () => import('../views/Index.vue')
  },
  {
    path: '/account',
    name: 'Account',
    component: () => import('../views/Account.vue')
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('../views/Categories.vue')
  },
  {
    path: '/categories/:id',
    name: 'Category',
    component: () => import('../views/Category.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  mode: 'history',
  routes
})

export default router
