<template>
  <div class="auth">
    <div class="container">
      <div class="auth__body">
        <h1 class="auth__title">
          Зарегистрироваться
        </h1>

        <form
          class="auth__form"
          autocomplete="off"
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
            <!-- <div class="auth__row">
              <UIBaseInput
                v-model="form.name"
                label="Имя и фамилия"
                placeholder="Укажите имя, фамилию"
              />
            </div> -->
            <div class="auth__row">
              <UIBaseInput
                v-model="form.first_name"
                label="Имя"
                placeholder="Укажите имя"
                required
              />
            </div>

            <div class="auth__row">
              <UIBaseInput
                v-model="form.last_name"
                label="Фамилия"
                placeholder="Укажите фамилию"
                required
              />
            </div>

            <div class="auth__row">
              <UIBaseInput
                v-model="form.email"
                label="E-mail"
                placeholder="Укажите e-mail"
                type="email"
                required
              />
            </div>

            <div class="auth__row">
              <UIBaseInput
                v-model="form.username"
                label="Username"
                placeholder="Укажите username"
                required
              />
            </div>

            <!-- <div class="auth__row">
              <UIBaseInput
                v-model="form.phone"
                type="tel"
                label="Телефон"
                placeholder="+7 (___) ___-__-__"
              />
            </div> -->

            <div class="auth__row">
              <UIBaseInput
                v-model="form.password"
                label="Пароль"
                type="password"
                required
              />
            </div>

            <div class="auth__row">
              <UIBaseInput
                v-model="form.password_confirm"
                label="Повторите пароль"
                type="password"
                required
              />
            </div>
          </div>

          <UIBaseButton
            type="submit"
            text="Зарегистрироваться"
            full-width
            :loading="isLoading"
            :disable="isLoading"
            class="auth__btn auth__btn--sign-up"
          />

          <p class="auth__conditions">
            Нажимая на кнопку «Зарегистрироваться», вы соглашаетесь с
            <a
              href="#"
              @click.prevent=""
            >
              условиями пользовательского соглашения
            </a>
          </p>

          <div class="auth__links">
            <p>
              У вас уже есть аккаунт?
              <NuxtLink to="/sign-in" class="auth__link">
                Войдите
              </NuxtLink>
            </p>
          </div>
        </form>

        <CommonContactsBlock
          class="auth__contacts"
        />
      </div>
    </div>

    <ModalsSuccessSignUp
      v-if="isShowSuccessSignUp"
      @close="isShowSuccessSignUp = false, navigateTo('/lk/profile')"
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
const isShowSuccessSignUp = ref(false)
const form = reactive({
  email: '',
  username: '',
  // phone: '',
  // name: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: '',
})

const onSubmit = async () => {
  isLoading.value = true
  const { data } = await useFetch('/api/auth/signup', {
    method: 'post',
    body: {
      ...form,
    },
    headers: useHeaderToken(),
  })
  isLoading.value = false

  if (data?.value?.status === 'success') {
    // setUser(data.value.user)
    await getUser()
    isShowSuccessSignUp.value = true
  } else {
    $toast.error(data?.value?.message)
  }
}

const socialAuth = () => {}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/auth.scss';
</style>
