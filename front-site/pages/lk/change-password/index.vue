<template>
  <div class="change-password">
    <div class="container-lk container-lk--profile">
      <div class="change-password__box">
        <h1 class="change-password__title">
          Изменить пароль
        </h1>

        <form
          class="change-password__form"
          @submit.prevent="onSubmit"
        >
          <div class="change-password__rows">
            <UIBaseInput
              v-model="form.password"
              label="Текущий пароль"
              required
              type="password"
            />
            <UIBaseInput
              v-model="form.new_password"
              label="Новый пароль"
              required
              type="password"
            />
          </div>

          <UILkButton
            type="submit"
            text="Сохранить"
            full-width
            is-big
            class="change-password__btn"
          />
        </form>
      </div>
    </div>

    <ModalsSuccessChangePassword
      v-if="isShowSuccessChangePasswordModal"
      @close="isShowSuccessChangePasswordModal = false"
    />
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user.js'

definePageMeta({
  layout: 'lk',
})

const { user } = storeToRefs(useUserStore())

const isShowSuccessChangePasswordModal = ref(false)
const form = reactive({
  password: '',
  new_password: '',
})

const onSubmit = async () => {
  const { data, error } = await useFetch(`/api/account/${user.value.id}/password`, {
    method: 'post',
    body: {
      ...form,
    },
    headers: useHeaderToken(),
  })

  const isNotValid = error?.value?.status

  if (isNotValid) {
    return false
  }
  form.password = ''
  form.new_password = ''

  isShowSuccessChangePasswordModal.value = true
}
</script>

<style lang="scss" scoped>
.change-password {
  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 60px;
  }

  &__title {
    margin-bottom: 32px;
    font-weight: 600;
    font-size: 32px;
    line-height: 40px;
  }

  &__form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 740px;
    padding: 40px 140px;
    background: var(--white);
    border-radius: 16px;
  }

  &__rows {
    display: grid;
    grid-gap: 20px;
    width: 100%;
  }

  &__btn {
    max-width: 200px;
    margin-top: 32px;
  }
}
</style>
