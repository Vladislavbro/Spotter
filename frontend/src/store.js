import Vuex from 'vuex'
import {app} from './main'
import {api} from './api'
const store = new Vuex.Store({
  state: {
    user: {},
    auth: 'login',

    topCategoriesParams: {
      model: 'categories',
      page: 1,
      sort: 'top'
    },
    total: 0,
    topCategories: [],
    categories: [],
    category: {},
    products: [],
    info: null,
  },
  mutations: {
    mergeStore (state, data) {
      for (const key of Object.keys(data)) {
        state[key] = data[key]
      }
    },
    setUser (state, data) {
      state.user = data
    },
    setData (state, {attr, value}) {
      state[attr] = value
    },
    addData (state, {attr, value}) {
      state[attr].push(value)
    },
  },
  actions: {

    async getTopCategories (context) {
      try {
        const response = await api.getTopCategories(context)
        if (response.status === 200 && response.data) {
          context.commit('mergeStore', {
            topCategories: response.data.items,
            total: response.data.total
          })
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async getCategories (context) {
      try {
        const response = await api.getCategories()
        if (response.status === 200 && response.data) {
          context.commit('mergeStore', {categories: response.data.categories})
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async getCategory (context, id) {
      try {
        const response = await api.getCategory(id)
        if (response.status === 200 && response.data) {
          context.commit('mergeStore', {
            category: response.data.category,
            products: response.data.products,
            info: response.data.info,
          })
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async getProducts (context) {
      try {
        const response = await api.getProducts(context)
        if (response.status === 200 && response.data) {
          context.commit('setData', {attr: 'products', value: response.data.products})
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async saveCategory (context) {
      try {
        const response = await api.saveCategory(context)
        if (response.status === 200 && response.data) {
          // context.commit('addData', {attr: 'brands', value: response.data})
          app.$toast.success('Категория сохранена')
          context.dispatch('getCategories')
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async deleteCategory (context) {
      try {
        const response = await api.deleteCategory(context)
        if (response.status === 200) {
          context.dispatch('getCategories')
        }
      } catch (e) {
        app.$toast.error(`${e.type}: ${e.message}`)
      }
    },

    async signup (context) {
      try {
        const response = await api.signup(context)
        if (response.status === 200 && response.data.status === 'success') {
          context.state.auth = 'login'
          app.$toast.success('Успешная регистрация!', {duration: 2000})
          setTimeout(() => {
            location.replace('/')
          }, 2000)
        } else {
          app.$toast.error(response.data.message)
        }
      } catch (e) {
        app.$toast.error(`${e.name}: ${e.message}`)
      }
    },

    async login (context) {
      try {
        const response = await api.login(context)
        if (response.status === 200 && response.data) {
          context.dispatch('getUser')
        } else {
          app.$toast.error(`Что то пошло не так`)
        }
      } catch (e) {
        app.$toast.error(`${e.name}: ${e.message}`)
      }
    },

    async getUser (context) {
      try {
        const response = await api.getMe()
        if (response.data) {
          context.commit('setUser', response.data)
          context.dispatch('getCategories')
        }
      } catch (e) {
        // app.toasted.error(`${e.name}: ${e.message}`)
      }
    },

    async logout (context) {
      try {
        const response = await api.logout(context)
        if (response.status === 200) {
          context.commit('mergeStore', {user: {}})
          location.reload()
        }
      } catch (e) {
        app.$toast.error(`${e.name}: ${e.message}`)
      }
    },

  }
})

export {
  store
}
