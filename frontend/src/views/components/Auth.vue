<template>
  <div class="d-flex">
    <div id="auth-card" class="card card-body my-auto mx-auto">

      <div v-if="$store.state.auth === 'login'">
        <form @submit.prevent="$store.dispatch('login')" id="login-form" class="mb-3">
          <div class=" mb-3">
            <label for="">Логин</label>
            <input
              id="input-auth-login"
              class="form-control"
              v-model="$store.state.user.username"
              placeholder=""
              required />
          </div>

          <div class="mb-4 ">
            <label for="">Пароль</label>
            <input
              id="input-auth-password"
              class="form-control"
              v-model="$store.state.user.password"
              placeholder="Пароль"
              type="password"
              required />
          </div>

          <button id="input-auth-submit" type="submit" class="btn btn-primary btn-lg btn-block">Вход</button>
        </form>
        <div class="text-center">
          <button
            id="auth-signup-btn-one"
            class="btn btn-link py-0 fs-18"
            @click="$store.commit('mergeStore', {auth: 'signup'})">
            Регистрация нового аккаунта
          </button>
        </div>
      </div>

      <div v-else-if="$store.state.auth === 'signup'" class="">
        <div class="mb-3">
          <label for="">Логин</label>
          <input
            id="signup-username-input"
            class="form-control"
            v-model="$store.state.user.username"
            placeholder="Логин"
            required />
        </div>
        <div class="mb-3">
          <label for="">Email</label>
          <input
            id="signup-email-input"
            class="form-control"
            v-model="$store.state.user.email"
            placeholder="Email"
            type="email" />
        </div>
        <div class="mb-3">
          <label for="">Имя</label>
          <input
            id="signup-first_name-input"
            class="form-control"
            v-model="$store.state.user.first_name"
            placeholder="Имя"
            type="text" />
        </div>
        <div class="mb-3">
          <label for="">Фамилия</label>
          <input
            id="signup-last_name-input"
            class="form-control"
            v-model="$store.state.user.last_name"
            placeholder="Фамилия"
            type="text" />
        </div>
        <div class="mb-3">
          <label for="">Пароль</label>
          <input
            id="signup-password-input"
            class="form-control"
            v-model="$store.state.user.password"
            placeholder="Пароль"
            type="password" />
        </div>
        <div class="mb-3">
          <label for="">Пароль еще раз</label>
          <input
            id="signup-password-confirm-input"
            class="form-control"
            v-model="$store.state.user.password_confirm"
            placeholder="Пароль еще раз"
            type="password" />
        </div>
        <button id="signup-submit" @click="signup" class="btn btn-primary btn-lg btn-block mb-4">Регистрация</button>
        <div class="text-center">
          <button
            id="auth-signup-btn-one"
            class="btn btn-link py-0 fs-18"
            @click="$store.commit('mergeStore', {auth: 'login'})">
            Вход с существующим аккаунтом
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>

export default {
  name: 'Auth',

  methods: {

    signup () {
      // if (!this.$store.state.user.username) {
      //   return this.$toast.error('username')
      // }
      if (!this.$store.state.user.email) {
        return this.$toast.error('email')
      }
      if (!this.$store.state.user.password) {
        return this.$toast.error('password')
      }
      if (!this.$store.state.user.first_name) {
        return this.$toast.error('first_name')
      }
      if (!this.$store.state.user.last_name) {
        return this.$toast.error('last_name')
      }
      if (!this.$store.state.user.password_confirm) {
        return this.$toast.error('password_confirm')
      }
      if (this.$store.state.user.password != this.$store.state.user.password_confirm) {
        return this.$toast.error('Пароли не совпадают')
      }
      this.$store.dispatch('signup')
    }
  }
}
</script>


<style lang="scss">
</style>
