import { defineStore } from 'pinia'
import { appendResponseHeader } from 'h3'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    user: null,
  }),
  actions: {
    async getUser (event) {
      const { data, error } = await useFetch('/api/auth/me', {
        suspense: true, // mode to defer rendering until the data is available
        server: true,
        onResponse ({ response }) {
          const setCookie = (response.headers.get('set-cookie') || '')
          if (setCookie) {
            const cookiesArray = setCookie.split('sessionid')
            if (cookiesArray[1]) {
              cookiesArray[1] = 'sessionid' + cookiesArray[1]
            }

            cookiesArray.forEach((item) => {
              appendResponseHeader(event, 'set-cookie', item)
            })
          }
        },
      })

      if (data?.value?.id) {
        this.user = data.value
      }
    },

    setUser (data) {
      this.user = data
    },

    async userLogOut () {
      await useFetch('/api/auth/log_out')

      this.user = null
    },
  },

  getters: {
    isAuth: state => !!state.user,

    isAdmin: state => !!state.user?.is_superuser,
  },
})
