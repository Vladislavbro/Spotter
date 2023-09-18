import { useUserStore } from '@/store/user.js'

export default defineNuxtPlugin(async (nuxtApp) => {
  const event = useRequestEvent()
  const user = useUserStore(nuxtApp.$pinia)

  await user.getUser(event)
})
