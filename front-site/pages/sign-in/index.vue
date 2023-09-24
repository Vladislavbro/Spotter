<template>
  <div class="auth">
    <div class="container">
      <div class="auth__body">
        <h1 class="auth__title">
          Вход
        </h1>

        <form
          class="auth__form"
          @submit.prevent="onSubmit"
        >
          <div class="auth__socials">
            <a
              v-for="(item, i) in socials"
              :key="i"
              href="#"
              class="auth__social"
              @click.prevent="socialAuth()"
            >
              <UIBaseIcon :name="item.icon" />
            </a>
          </div>

          <div class="auth__rows">
            <div class="auth__row">
              <UIBaseInput
                v-model="form.email"
                label="Username"
              />
            </div>

            <div class="auth__row">
              <UIBaseInput
                v-model="form.password"
                label="Пароль"
                type="password"
              />
            </div>
          </div>

          <UIBaseButton
            type="submit"
            text="Войти"
            full-width
            :loading="isLoading"
            :disable="isLoading"
            class="auth__btn"
          />

          <div class="auth__links">
            <a
              href="/"
              class="auth__link"
              @click.prevent="isShowRestorePassword = true"
            >
              Забыли пароль?
            </a>
            <p>
              У вас еще нет аккаунта?
              <NuxtLink to="/sign-up" class="auth__link">
                Зарегистрируйтесь
              </NuxtLink>
            </p>
          </div>
        </form>

        <CommonContactsBlock
          class="auth__contacts"
        />
      </div>
    </div>

    <ModalsRestorePassword
      v-if="isShowRestorePassword"
      @close="isShowRestorePassword = false"
    />
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const { $toast } = useNuxtApp()

const user = useUserStore()
const { getUser } = user

const socials = [
  // { icon: 'auth/icon-yandex' },
  // { icon: 'auth/icon-google' },
  { icon: 'auth/icon-vk' },
]

const isLoading = ref(false)
const isShowRestorePassword = ref(false)
const form = reactive({
  email: '',
  password: '',
})

const onSubmit = async () => {
  isLoading.value = true
  const { data } = await useFetch('/api/auth/log_in', {
    method: 'post',
    body: {
      ...form,
    },
    headers: useHeaderToken(),
  })
  isLoading.value = false

  if (data?.value && (!data?.value?.status || data?.value?.status !== 'not auth')) {
    // setUser(data.value)
    await getUser()
    navigateTo('/lk/profile')
  } else {
    $toast.error(data?.value?.message || 'Пользователь не найден')
  }
}

const socialAuth = () => {}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/auth.scss';
</style>
