<template>
  <div class="auth">
    <div class="container">
      <div class="auth__body">
        <h1 class="auth__title">
          Новый пароль
        </h1>

        <transition name="fade" mode="out-in">
          <form
            v-if="!isSuccess"
            class="auth__form"
            @submit.prevent="onSubmit"
          >
            <div class="auth__rows">
              <div class="auth__row">
                <UIBaseInput
                  v-model="form.password"
                  label="Укажите новый пароль"
                  type="password"
                />
              </div>
            </div>

            <UIBaseButton
              type="submit"
              text="Сменить пароль"
              full-width
              class="auth__btn"
            />
          </form>

          <div
            v-else
            class="auth__success"
          >
            <div class="auth__success-icon">
              <UIBaseIcon name="landing/icon-galka" />
            </div>
            <p class="auth__text">
              Пароль успешно изменен!
            </p>
            <UIBaseButton
              to="/sign-in"
              text="Войти"
              full-width
              class="auth__btn auth__btn--success"
            />
          </div>
        </transition>

        <AuthContacts class="auth__contacts" />
      </div>
    </div>
  </div>
</template>

<script setup>
const isSuccess = ref(false)
const form = reactive({
  password: '',
})

const onSubmit = () => {
  isSuccess.value = true
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/auth.scss'
</style>
