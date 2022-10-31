<template lang="html">
  <div class="container">
    <div class="d-flex my-4">
      <div class="me-auto">
        <h3>Категории</h3>
      </div>
      <div class="">
        <button
          class="btn btn-sm btn-light"
          data-bs-toggle="modal"
          data-bs-target="#categoryModal"
          @click="$store.commit('setData', {attr: 'category', value: {name: '', slug: '', k: 1, subjects: ''}})">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
          </svg>
        </button>
      </div>
    </div>

    <div
      v-for="category in $store.state.categories"
      :key="category._id.$oid"
      class="mb-2">
      <CategoryItem :category="category"/>
    </div>


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
import CategoryItem from './components/CategoryItem'
export default {
  name: 'Brands',
  components: {
    CategoryItem
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
      await this.$store.dispatch('getCategories')
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
