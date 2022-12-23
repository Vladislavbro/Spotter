<template lang="html">
  <div class="container-fluid">
    <div class="d-flex py-3">
      <div class="me-auto">
        <h3>Топ категорий</h3>
      </div>
      <div class="form-check me-3">
        <input
          @change="getData"
          value="queries"
          v-model="$store.state.topCategoriesParams.model"
          class="form-check-input"
          type="radio"
          name="model"
          id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
          Ниши
        </label>
      </div>
      <div class="form-check">
        <input
          @change="getData"
          value="categories"
          v-model="$store.state.topCategoriesParams.model"
          class="form-check-input"
          type="radio"
          name="model"
          id="flexRadioDefault2">
        <label class="form-check-label" for="flexRadioDefault2">
          Категории
        </label>
      </div>
    </div>

    <!-- "В этой странице открывается таблица с лучшими категориями товаров
    Категории отбираются согласно разделу анализ ниши
    Какие данные отражаются в таблице с подборкой:
    9. Среднее количество продаж на один товар
    10. Среднее количество продаж на одного продавца" -->

    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Название</th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('top')">
                Топ
              </button>
            </th>
            <th v-if="params.model == 'categories'">
              <button
                class="btn btn-link"
                @click="sortItems('products_count')">
                Товаров
              </button>
            </th>
            <th v-if="params.model == 'categories'">
              <button
                class="btn btn-link"
                @click="sortItems('sellers')">
                Продавцов
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('profit_prev_period')">
                Оборот пред. период
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('profit_period')">
                Оборот
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('first_product_decada_profit')">
                Оборот 1-го
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('ten_product_decada_profit')">
                Оборот 10-го
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('avg_price_period')">
                Средняя цена
              </button>
            </th>
            <th v-if="params.model == 'categories'">
              <button
                class="btn btn-link"
                @click="sortItems('sellers_with_sales')">
                Продавцы с продажами
              </button>
            </th>
            <th>
              <button
                class="btn btn-link"
                @click="sortItems('products_with_sales')">
                Товары с продажами
              </button>
            </th>
            <th v-if="params.model == 'categories'">
              <button
                class="btn btn-link"
                @click="sortItems('sales_period')">
                Продаж
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="category in $store.state.topCategories"
            :class="{
              'table-success': category.top
            }"
            :key="category.id">
            <td>
              <a :href="'https://www.wildberries.ru' + category.url" target="_blank">{{ category.name }}</a>
            </td>
            <td>{{ category.top }}</td>
            <td v-if="params.model == 'categories'">{{ category.products_count }}</td>
            <td v-if="params.model == 'categories'">{{ category.sellers }}</td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.profit_prev_period) }}
            </td>
            <td>{{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.profit_period) }}</td>
            <td>{{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.first_product_decada_profit) }}</td>
            <td>{{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.ten_product_decada_profit) }}</td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.avg_price_period) }}
            </td>
            <td v-if="params.model == 'categories'">{{ category.sellers_with_sales }}</td>
            <td>{{ category.products_with_sales }}</td>
            <td v-if="params.model == 'categories'">{{ category.sales_period }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <pagination
      v-model="$store.state.topCategoriesParams.page"
      :records="$store.state.total"
      :per-page="100"
      :options="{
        theme: 'bootstrap3',
        texts: {
          count: 'Показано с {from} до {to} из {count} записей|{count} запись|Одна запись',
          first: 'Первая',
          last: 'Последняя',
        }
      }"
      @paginate="$store.dispatch('getTopCategories')"
    />

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
import Pagination from 'v-pagination-3'
export default {
  name: 'Index',
  components: {
    Pagination,
  },
  computed: {
    params () {
      return this.$store.state.topCategoriesParams
    },
  },

  methods: {
    sortItems (sort) {
      this.$store.commit('mergeStore', {
        topCategoriesParams: {
          ...this.$store.state.topCategoriesParams,
          sort
        }
      })
      this.$store.dispatch('getTopCategories')
    },
    getData () {
      this.$store.commit('mergeStore', {
        topCategoriesParams: {
          ...this.$store.state.topCategoriesParams,
          page: 1,
        }
      })
      this.$store.dispatch('getTopCategories')
    },
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
