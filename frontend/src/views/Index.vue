<template lang="html">
  <div class="container-fluid">
    <div class="d-flex py-3">
      <div class="">
        <h3>Топ ниши</h3>
      </div>

      <div class="mx-auto">
        <a href="/api/export/categories" class="btn btn-light" v-if="$store.state.user.is_superuser">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-csv" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.517 14.841a1.13 1.13 0 0 0 .401.823c.13.108.289.192.478.252.19.061.411.091.665.091.338 0 .624-.053.859-.158.236-.105.416-.252.539-.44.125-.189.187-.408.187-.656 0-.224-.045-.41-.134-.56a1.001 1.001 0 0 0-.375-.357 2.027 2.027 0 0 0-.566-.21l-.621-.144a.97.97 0 0 1-.404-.176.37.37 0 0 1-.144-.299c0-.156.062-.284.185-.384.125-.101.296-.152.512-.152.143 0 .266.023.37.068a.624.624 0 0 1 .246.181.56.56 0 0 1 .12.258h.75a1.092 1.092 0 0 0-.2-.566 1.21 1.21 0 0 0-.5-.41 1.813 1.813 0 0 0-.78-.152c-.293 0-.551.05-.776.15-.225.099-.4.24-.527.421-.127.182-.19.395-.19.639 0 .201.04.376.122.524.082.149.2.27.352.367.152.095.332.167.539.213l.618.144c.207.049.361.113.463.193a.387.387 0 0 1 .152.326.505.505 0 0 1-.085.29.559.559 0 0 1-.255.193c-.111.047-.249.07-.413.07-.117 0-.223-.013-.32-.04a.838.838 0 0 1-.248-.115.578.578 0 0 1-.255-.384h-.765ZM.806 13.693c0-.248.034-.46.102-.633a.868.868 0 0 1 .302-.399.814.814 0 0 1 .475-.137c.15 0 .283.032.398.097a.7.7 0 0 1 .272.26.85.85 0 0 1 .12.381h.765v-.072a1.33 1.33 0 0 0-.466-.964 1.441 1.441 0 0 0-.489-.272 1.838 1.838 0 0 0-.606-.097c-.356 0-.66.074-.911.223-.25.148-.44.359-.572.632-.13.274-.196.6-.196.979v.498c0 .379.064.704.193.976.131.271.322.48.572.626.25.145.554.217.914.217.293 0 .554-.055.785-.164.23-.11.414-.26.55-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.764a.799.799 0 0 1-.118.363.7.7 0 0 1-.272.25.874.874 0 0 1-.401.087.845.845 0 0 1-.478-.132.833.833 0 0 1-.299-.392 1.699 1.699 0 0 1-.102-.627v-.495Zm8.239 2.238h-.953l-1.338-3.999h.917l.896 3.138h.038l.888-3.138h.879l-1.327 4Z"/>
          </svg>
          Путь 1
        </a>
        <a href="/api/export/queries" class="btn btn-light me-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-csv" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.517 14.841a1.13 1.13 0 0 0 .401.823c.13.108.289.192.478.252.19.061.411.091.665.091.338 0 .624-.053.859-.158.236-.105.416-.252.539-.44.125-.189.187-.408.187-.656 0-.224-.045-.41-.134-.56a1.001 1.001 0 0 0-.375-.357 2.027 2.027 0 0 0-.566-.21l-.621-.144a.97.97 0 0 1-.404-.176.37.37 0 0 1-.144-.299c0-.156.062-.284.185-.384.125-.101.296-.152.512-.152.143 0 .266.023.37.068a.624.624 0 0 1 .246.181.56.56 0 0 1 .12.258h.75a1.092 1.092 0 0 0-.2-.566 1.21 1.21 0 0 0-.5-.41 1.813 1.813 0 0 0-.78-.152c-.293 0-.551.05-.776.15-.225.099-.4.24-.527.421-.127.182-.19.395-.19.639 0 .201.04.376.122.524.082.149.2.27.352.367.152.095.332.167.539.213l.618.144c.207.049.361.113.463.193a.387.387 0 0 1 .152.326.505.505 0 0 1-.085.29.559.559 0 0 1-.255.193c-.111.047-.249.07-.413.07-.117 0-.223-.013-.32-.04a.838.838 0 0 1-.248-.115.578.578 0 0 1-.255-.384h-.765ZM.806 13.693c0-.248.034-.46.102-.633a.868.868 0 0 1 .302-.399.814.814 0 0 1 .475-.137c.15 0 .283.032.398.097a.7.7 0 0 1 .272.26.85.85 0 0 1 .12.381h.765v-.072a1.33 1.33 0 0 0-.466-.964 1.441 1.441 0 0 0-.489-.272 1.838 1.838 0 0 0-.606-.097c-.356 0-.66.074-.911.223-.25.148-.44.359-.572.632-.13.274-.196.6-.196.979v.498c0 .379.064.704.193.976.131.271.322.48.572.626.25.145.554.217.914.217.293 0 .554-.055.785-.164.23-.11.414-.26.55-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.764a.799.799 0 0 1-.118.363.7.7 0 0 1-.272.25.874.874 0 0 1-.401.087.845.845 0 0 1-.478-.132.833.833 0 0 1-.299-.392 1.699 1.699 0 0 1-.102-.627v-.495Zm8.239 2.238h-.953l-1.338-3.999h.917l.896 3.138h.038l.888-3.138h.879l-1.327 4Z"/>
          </svg>
          Скачать файл
        </a>
      </div>


      <!-- <div class="form-check me-3">
        <input
          @change="getData"
          value="categories"
          v-model="$store.state.topCategoriesParams.model"
          class="form-check-input"
          type="radio"
          name="model"
          id="flexRadioDefault2">
        <label class="form-check-label" for="flexRadioDefault2">
          Путь 1
        </label>
      </div>
      <div class="form-check">
        <input
          @change="getData"
          value="queries"
          v-model="$store.state.topCategoriesParams.model"
          class="form-check-input"
          type="radio"
          name="model"
          id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
          Путь 2
        </label>
      </div> -->
    </div>

    <div class="table-wrapper">
      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Название</th>
            <th v-if="params.model == 'queries'">Характеристики</th>
            <th>
              Товаров
            </th>
            <th>
              Товары с продажами
            </th>
            <th>
              Товары с продажами
            </th>
            <th>
              Оборот 1-го
            </th>
            <th>
              Оборот 10-го
            </th>
            <th>
              Средняя цена пред
            </th>
            <th>
              Средняя цена тек
            </th>
            <th>Изм средней цены</th>
            <th>
              Оборот пред. период
            </th>
            <th>
              Оборот
            </th>
            <th>
              Изменение оборота
            </th>
            <th v-if="params.model == 'categories'">
              Продавцов
            </th>
            <th v-if="params.model == 'categories'">
              Продавцы с продажами
            </th>
            <th v-if="params.model == 'categories'">
              Продавцы с продажами
            </th>
            <th v-if="params.model == 'categories'">
              Продаж
            </th>
            <th>
              Топ
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="category in $store.state.topCategories"
            :key="category.id">
            <td>
              <a
                v-if="category.url"
                :href="'https://www.wildberries.ru' + category.url"
                target="_blank">
                {{ category.name }}
              </a>
              <a
                v-else
                :href="getQueryUrl(category)"
                target="_blank">
                {{ category.root }}
              </a>
            </td>
            <td v-if="params.model == 'queries'">{{ category.features }}</td>
            <td>
              {{ new Intl.NumberFormat('ru-RU').format(category.products_count) }}
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU').format(category.products_with_sales) }}
            </td>
            <td>
              <!-- <span v-if="category.products_count">{{ (category.products_with_sales * 100 / category.products_count).toFixed() }} %</span> -->
              <span v-if="category.products_count">{{ category.rel_products_with_sales }} %</span>
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.first_product_decada_profit) }}
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.ten_product_decada_profit) }}
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.avg_price_prev_period) }}
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.avg_price_period) }}
            </td>
            <td>
              <span v-if="category.avg_price_prev_period">{{ (category.avg_price_period * 100 / category.avg_price_prev_period).toFixed() }} %</span>
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.profit_prev_period) }}
            </td>
            <td>
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(category.profit_period) }}
            </td>
            <td>
              <span v-if="category.profit_prev_period">{{ (category.profit_period * 100 / category.profit_prev_period).toFixed() }} %</span>
            </td>
            <td v-if="params.model == 'categories'">
              {{ new Intl.NumberFormat('ru-RU').format(category.sellers) }}
            </td>
            <td v-if="params.model == 'categories'">
              {{ new Intl.NumberFormat('ru-RU').format(category.sellers_with_sales) }}
            </td>
            <td v-if="params.model == 'categories'">
              <span v-if="category.sellers">
                {{ (category.sellers_with_sales * 100 / category.sellers).toFixed() }} %
              </span>
            </td>
            <td v-if="params.model == 'categories'">
              {{ new Intl.NumberFormat('ru-RU').format(category.sales_period) }}
            </td>
            <td>{{ category.top }}</td>
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
    getQueryUrl (query) {
      return 'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=' + query.name.replaceAll(' ', '+')
    },
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
.table-wrapper{
  width: 100%;
  max-width: 100%;
  overflow: scroll;
}
table{
  thead{
    th{
      position: sticky;
      top: 0;
      background: white;
    }
  }
}
</style>
