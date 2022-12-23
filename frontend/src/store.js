import Vuex from 'vuex'
import {app} from './main'
import {api} from './api'
const store = new Vuex.Store({
  state: {
    topCategoriesParams: {
      model: 'queries',
      page: 1,
      // sort: 'ten_product_decada_profit'
    },
    total: 0,
    topCategories: [],
    categories: [],
    category: {},
    products: [],
    groups: [],
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
            groups: response.data.groups,
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

    async login (context) {
      try {
        const response = await api.login(context)
        if (response.status === 200 && response.data) {
          context.dispatch('getUser')
        }
      } catch (e) {
        // app.toasted.error(`${e.name}: ${e.message}`)
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

  }
})

export {
  store
}
