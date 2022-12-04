<template lang="html">
  <div class="container-xl">
    <div class="d-flex my-4">
      <div class="me-auto">
        <h3>Топ категорий</h3>
      </div>
    </div>

    <!-- "В этой странице открывается таблица с лучшими категориями товаров
    Категории отбираются согласно разделу анализ ниши
    Какие данные отражаются в таблице с подборкой:
    9. Среднее количество продаж на один товар
    10. Среднее количество продаж на одного продавца" -->

    <table class="table table-bordered table-hover">
      <thead>
        <tr>
          <th>Название</th>
          <th>Товаров</th>
          <th>Продавцов</th>
          <th>Оборот</th>
          <th>Средняя цена</th>
          <th>Продавцы с продажами</th>
          <th>Товары с продажами</th>
          <th>Продаж</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="category in $store.state.topCategories"
          :key="category._id.$oid">
          <td>
            <a :href="'https://www.wildberries.ru' + category.url" target="_blank">{{ category.name }}</a>
          </td>
          <td>{{ category.products_count }}</td>
          <td>{{ category.sellers }}</td>
          <td>
            {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.profit_period) }}
          </td>
          <td>
            {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.avg_price_period) }}
          </td>
          <td>{{ (category.rel_sellers * 100).toFixed() }}<small class="text-black-50"> %</small></td>
          <td>{{ (category.rel_sales * 100).toFixed() }}<small class="text-black-50"> %</small></td>
          <td>{{ category.sales_period }}</td>
        </tr>
      </tbody>
    </table>

    <div class="modal fade" id="categoryModal" tabindex="-1" aria-labelledby="categoryModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="$store.dispatch('saveCategory')">
            <div class="modal-header">
              <h5 class="modal-title" id="categoryModalLabel">{{ $store.state.category.name }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="input-category-name" class="form-label">Название</label>
                <input type="text" v-model="$store.state.category.name" class="form-control" id="input-category-name">
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Сохранить</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: 'Brands',
  components: {

  },
  computed: {
    getBrands () {
      return this.$store.state.brands.filter(b => !b.exclude)
    },

    getExcludeBrands () {
      return this.$store.state.brands.filter(b => b.exclude)
    },
  },

  methods: {
    deleteCategory (category) {
      if (confirm('Удалить категорию?')) {
        this.$store.commit('setData', {attr: 'category', value: category})
        this.$store.dispatch('deleteCategory')
      }
    }
  },

  async mounted () {
    try {
      await this.$store.dispatch('getTopCategories')
      // this.$store.commit('setData', {attr: 'category', value: this.$store.state.categories[0]})
    } catch (e) {
      console.error(e)
      // this.$toasted.error(`${e.type}: ${e.message}`)
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
