<template>
  <main>
    <div v-if="$store.state.user.id" class="">
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
                <router-link :to="{ name: 'Categories', params: {} }" class="nav-link">Категории</router-link>
              </li>
              <li class="nav-item" v-if="$store.state.user.is_superuser">
                <router-link :to="{ name: 'Accounts', params: {} }" class="nav-link">Пользователи</router-link>
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
              <li class="nav-item">
                <router-link :to="{name: 'Account'}" class="nav-link">{{ $store.state.user.username }}</router-link>
              </li>
              <span class="navbar-text me-3 text-black-50">
                <i>{{ getSubPeriod }}</i>
              </span>
              <button @click="$store.dispatch('logout')" class="btn btn-outline-secondary">Выход</button>
            </ul>
          </div>
        </div>
      </nav>
      <router-view/>
    </div>
    <div v-else class="min-h-100-vh d-flex align-items-center justify-content-center">
      <Auth />
    </div>
  </main>
</template>

<script>
import Auth from './views/components/Auth'
export default {
  name: "Index",
  components: {
    Auth,
  },
  computed: {
    getSubPeriod () {
      if (this.$store.state.user.customer__subscribe_until) {
        return '(10 дней до конца подписки)'
      } else {
        return '(без подписки)'
      }
    }
  },
  async mounted () {
    try {
      // this.$store.dispatch('getData')
      this.$store.dispatch('getUser')
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
.min-h-100-vh{
  min-height: 100vh;
}
</style>
