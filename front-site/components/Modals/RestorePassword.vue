<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="restore-password">
      <p class="restore-password__title">
        Восстановление пароля
      </p>

      <transition name="fade" mode="out-in">
        <form
          v-if="!isSuccess"
          class="restore-password__form"
          @submit.prevent="onSubmit()"
        >
          <div class="restore-password__row">
            <UIBaseInput
              v-model="form.email.value"
              :error="form.email.error"
              type="email"
              label="E-mail"
              required
              class="restore-password__input"
            />
          </div>

          <UIBaseButton
            type="submit"
            text="Отправить"
            full-width
            :loading="isLoading"
            :disable="isLoading"
            class="restore-password__btn"
          />

          <a
            href="#"
            class="restore-password__link"
            @click.prevent="closeModal()"
          >
            Вернуться к авторизации
          </a>
        </form>

        <div
          v-else
          class="restore-password__success"
        >
          <div class="restore-password__icon">
            <UIBaseIcon name="landing/icon-galka" />
          </div>

          <p class="restore-password__text">
            Мы отправили письмо с ссылкой для сброса пароля на ваш e-mail
          </p>

          <UIBaseButton
            text="Хорошо"
            full-width
            primary-black-outline
            class="restore-password__btn restore-password__btn--success"
            @click="closeModal()"
          />
        </div>
      </transition>
    </div>
  </ModalsLayout>
</template>

<script setup>
const emits = defineEmits(['close'])

const isLoading = ref(false)
const isSuccess = ref(false)
const form = reactive({
  email: {
    value: '',
    error: '',
  },
})

watch(() => form.email.value, () => {
  form.email.error = ''
})

const onSubmit = async () => {
  isLoading.value = true
  const { data } = await useFetch('/api/password', {
    query: {
      email: form.email.value,
    },
  })
  isLoading.value = false

  if (data?.value?.status === 'success') {
    isSuccess.value = true
  } else {
    form.email.error = data.value.message
  }
}

const closeModal = () => {
  emits('close')
}
</script>

<style lang="scss" scoped>
.restore-password {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(100vw - 20px - 20px);
  padding: 32px 24px 48px;
  color: var(--blackMain);
  background: #FFFFFF;
  border-radius: 12px;

  @include mq($bp-small) {
    width: 740px;
    padding: 40px 0 60px;
    border-radius: 16px;
  }

  &__title {
    @include h4;

    margin-bottom: 32px;
    text-align: center;

    @include mq($bp-small) {
      margin-bottom: 40px;
    }
  }

  &__form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  &__row {
    width: 100%;
    max-width: 460px;
  }

  &__btn {
    height: 44px;
    max-width: 200px;
    margin-top: 28px;

    @include mq($bp-small) {
      height: 56px;
      margin-top: 40px;
    }

    &--success {
      margin-top: 42px;

      @include mq($bp-small) {
        margin-top: 56px;
      }
    }
  }

  &__link {
    margin-top: 20px;
    color: var(--purple);
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;

    @include mq($bp-small) {
      font-size: 14px;
      line-height: 16px;
    }
  }

  &__success {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    margin-bottom: 12px;
    border: 1px solid var(--purple);
    border-radius: 50%;

    @include mq($bp-small) {
      width: 48px;
      height: 48px;
      margin-bottom: 16px;
    }

    ::v-deep(.ui-icon) {
      svg > * {
        fill: var(--purple);
      }
    }
  }

  &__text {
    @include text_normal;
  }
}
</style>
