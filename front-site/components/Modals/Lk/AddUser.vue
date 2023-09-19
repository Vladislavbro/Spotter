<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="add-user">
      <p class="add-user__title">
        Добавить аккаунт
      </p>

      <form
        class="add-user__form"
        @submit.prevent="onSubmit"
      >
        <UIBaseInput
          id="first_name"
          v-model="form.first_name"
          label="Имя"
          required
          placeholder="Укажите имя"
        />

        <UIBaseInput
          id="last_name"
          v-model="form.last_name"
          label="Фамилия"
          required
          placeholder="Укажите фамилию"
        />

        <UIBaseInput
          id="username"
          v-model="form.username"
          label="Username"
          required
          placeholder="Укажите username"
        />

        <UIBaseInput
          id="email"
          v-model="form.email"
          label="E-mail"
          required
          placeholder="Укажите e-mail"
          type="email"
        />

        <!-- <UIBaseInput
          id="phone"
          v-model="form.phone"
          label="Телефон"
          required
          placeholder="+7 (___) ___-__-__"
          type="tel"
        /> -->

        <UIBaseInput
          id="password"
          v-model="form.password"
          label="Пароль"
          required
          type="password"
        />

        <!-- <div class="add-user__status">
          <p class="add-user__status-label">
            Статус:
          </p>
          <UILkRadio
            id="status-pro"
            v-model="form.customer__subscribe_type"
            value="premium"
            text="Продвинутый"
          />
          <UILkRadio
            id="status-base"
            v-model="form.customer__subscribe_type"
            value="trial"
            text="Базовый"
          />
        </div>

        <UIBaseInput
          id="date"
          v-model="form.date"
          label="Подписка до"
          required
          placeholder="дд.мм.гггг"
        /> -->

        <UILkButton
          text="Добавить"
          type="submit"
          is-big
          full-width
          class="add-user__btn"
        />
      </form>
    </div>
  </ModalsLayout>
</template>

<script setup>
const emits = defineEmits(['close', 'success'])

const form = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  // phone: '',
  password: '',
  // customer__subscribe_type: 'premium',
  // date: '',
})

const closeModal = () => {
  emits('close')
}

const onSubmit = () => {
  emits('success', form)
  closeModal()
}
</script>

<style lang="scss" scoped>
.add-user {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 740px;
  padding: 40px 0 32px;
  color: var(--blackMain);
  background: #FFFFFF;
  border-radius: 16px;

  &__title {
    @include h4;

    margin-bottom: 28px;
    text-align: center;
  }

  &__form {
    width: 100%;
    max-width: 460px;
    display: grid;
    grid-gap: 12px;
  }

  &__status {
    display: grid;
    grid-template-columns: repeat(3, auto);
    grid-gap: 20px;
    align-items: center;
    justify-content: flex-start;
    margin: 8px 0;

    &-label {
      font-weight: 500;
      font-size: 14px;
      line-height: 18px;
    }
  }

  &__btn {
    max-width: 200px;
    margin: 20px auto 0;
  }
}
</style>
