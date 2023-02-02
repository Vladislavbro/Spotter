<template>
  <div class="container-fluid py-4">
    <h3>{{ $store.state.category.name }}</h3>
    <!-- <small>{{ $store.state.category }}</small> -->
    <div class="py-3 text-end">
      <!-- Товаров: <strong>{{ $store.state.info }}</strong> -->
    </div>
    <table class="table table-bordered table-hover">
      <thead>
        <th>Название товара</th>
        <th>
          <button
            class="btn btn-link"
            @click="sortItems('price')">
            Цена
          </button>
        </th>
        <th>
          <button
            class="btn btn-link"
            @click="sortItems('rating')">
            Рейтинг
          </button>
        </th>
        <th>Бренд</th>
        <th>
          <button
            class="btn btn-link"
            @click="sortItems('current_hom_profit')">
            Оборот в тек периоде
          </button>
        </th>
        <th>
          <button
            class="btn btn-link"
            @click="sortItems('current_hom_sales')">
            Продажи (шт.)
          </button>
        </th>
        <th>Дата</th>
      </thead>
      <tbody>
        <tr v-for="product in $store.state.products" :key="product.id">
          <td>
            <a
              :href="'https://www.wildberries.ru/catalog/' + product.articul + '/detail.aspx'"
              target="_blank">
              {{ product.name }}
            </a>
          </td>
          <td>{{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(product.price) }}</td>
          <td>{{ product.rating }}</td>
          <td>{{ product.brand }}</td>
          <td>
            {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(product.current_hom_profit) }}
            <!-- ({{ product.hom_profit_growth }}) -->
          </td>
          <td>{{ product.current_hom_sales }}</td>
          <td>{{ getPeriod(product) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import moment from 'moment'
moment.locale('ru')
export default {
  data () {
    return {
      id: null
    }
  },
  created: function () {
    this.moment = moment
  },
  methods: {
    sortItems (sort) {
      this.$store.commit('mergeStore', {
        categoryParams: {
          ...this.$store.state.categoryParams,
          sort
        }
      })
      this.$store.dispatch('getCategory', this.id)
    },
    getPeriod (product) {
      const start = this.moment(product.parsed_at.$date).subtract(15, 'days').format('LL')
      const end = this.moment(product.parsed_at.$date).format('LL')
      return `${start} - ${end}`
    },
    getProductUrl (product) {
      return `https://images.wbstatic.net/big/new/${product.articul.toString().substr(0, 4)}0000/${product.articul}-1.jpg`
    }
  },
  mounted () {
    this.$store.commit('mergeStore', {
      category: {},
      products: [],
    })
    this.id = this.$route.params.id
    this.$store.dispatch('getCategory', this.id)
  }
}
</script>

<style lang="css" scoped>
</style>
