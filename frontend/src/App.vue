<template>
  <main>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse w-100" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link :to="{ name: 'Index', params: {} }" class="nav-link">Топ категорий</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'TopProducts', params: {} }" class="nav-link">Топ товаров</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'Categories', params: {} }" class="nav-link">Категории</router-link>
            </li>
            <!-- <li class="nav-item">
              <router-link :to="{ name: 'Index', params: {} }" class="nav-link">Товары</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'Config', params: {} }" class="nav-link">Настройки</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'Users', params: {} }" class="nav-link">Пользователи бота</router-link>
            </li> -->
          </ul>
          <ul class="navbar-nav ms-auto">
            <span class="navbar-text">
              <strong class="me-2">Василий</strong>
              <i>10 дней до конца подписки</i>
            </span>
          </ul>
        </div>
      </div>
    </nav>
    <router-view/>
  </main>
</template>

<script>
export default {
  name: "Index",
  async mounted () {
    try {
      // this.$store.dispatch('getData')
    } catch (e) {
      this.$toasted.error(`${e.type}: ${e.message}`)
    }
  }
}
</script>

<style lang="scss">
@import '~bootstrap/scss/bootstrap';
@import '@/assets/extra.scss';
@import '~@hennge/vue3-pagination/dist/vue3-pagination.css';
</style>
