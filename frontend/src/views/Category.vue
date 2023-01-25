<template>
  <div class="container py-4">
    <h3>{{ $store.state.category.name }}</h3>
    <small>{{ $store.state.category }}</small>
    <div class="py-3 text-end">
      Товаров: <strong>{{ $store.state.info }}</strong>
    </div>
    <table class="table table-bordered table-hover">
      <thead>
        <th>Название товара</th>
        <th>Фото</th>
        <th>Рейтинг</th>
        <th>Продавец</th>
        <th>Оборот в тек периоде</th>
        <th>Продажи (в штуках)</th>
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
          <td>
            <img :src="getProductUrl(product)" height="60">
          </td>
          <td>{{ product.rating }}</td>
          <td>{{ product.brand }}</td>
          <td>{{ product.current_hom_profit }} ({{ product.hom_profit_growth }})</td>
          <td>{{ product.current_hom_sales }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
export default {
  methods: {
    getProductUrl (product) {
      return `https://images.wbstatic.net/big/new/${product.articul.toString().substr(0, 4)}0000/${product.articul}-1.jpg`
    }
  },
  mounted () {
    this.$store.commit('mergeStore', {
      category: {},
      products: [],
    })
    const id = this.$route.params.id
    this.$store.dispatch('getCategory', id)
  }
}
</script>

<style lang="css" scoped>
</style>
