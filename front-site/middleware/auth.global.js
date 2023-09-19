import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user'

export default defineNuxtRouteMiddleware((to) => {
  const { isAuth } = storeToRefs(useUserStore())

  if (!isAuth.value && to.path.includes('/lk')) {
    return navigateTo('/sign-in')
  } else if (isAuth.value && (to.path.includes('/sign-in') || to.path.includes('/sign-up'))) {
    return navigateTo('/lk')
  }
})
