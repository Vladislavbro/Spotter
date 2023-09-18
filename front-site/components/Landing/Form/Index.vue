<template>
  <div class="form">
    <div class="container">
      <div class="form__box">
        <div class="form__content">
          <p class="form__title">
            Находите новые товары быстро и&nbsp;экономьте свое время
          </p>
          <p class="form__text">
            Найдите прибыльные ниши и развивайте свой бизнес на&nbsp;маркетплейсе. Зарегистрируйтесь прямо сейчас, а&nbsp;мы укажем для вас точки роста.
          </p>
          <img
            src="@/assets/images/landing/form/graphic.png"
            alt=""
            class="form__image"
          >
        </div>

        <form
          class="form__form"
          @submit.prevent="onSubmit"
        >
          <div class="form__rows">
            <div class="form__row">
              <UIBaseInput
                v-model="form.name"
                label="Имя и фамилия"
                placeholder="Укажите имя, фамилию"
              />
            </div>
            <div class="form__row form__row--double">
              <UIBaseInput
                v-model="form.email"
                label="E-mail"
                placeholder="Укажите e-mail"
              />
              <UIBaseInput
                v-model="form.phone"
                type="tel"
                label="Телефон"
                placeholder="+7 (___) ___-__-__"
              />
            </div>
            <div class="form__row form__row--double">
              <UIBaseInput
                v-model="form.password"
                type="password"
                label="Пароль"
              />
              <UIBaseInput
                v-model="form.password_repeat"
                type="password"
                label="Повторите пароль"
              />
            </div>
          </div>
          <UIBaseButton
            text="Зарегистрироваться"
            type="submit"
            full-width
            class="form__btn"
          />
          <p class="form__note">
            Нажимая на кнопку «Зарегистрироваться», вы соглашаетесь с
            <a
              href="#"
              @click.prevent=""
            >
              условиями пользовательского соглашения
            </a>
          </p>
        </form>
      </div>
    </div>

    <ModalsSuccessSignUp
      v-if="isShowSuccessSignUp"
      @close="isShowSuccessSignUp = false"
    />
  </div>
</template>

<script setup>
const isShowSuccessSignUp = ref(false)
const form = reactive({
  name: '',
  email: '',
  phone: '',
  password: '',
  password_repeat: '',
})

const onSubmit = () => {
  isShowSuccessSignUp.value = true
}
</script>

<style lang="scss" scoped>
.form {
  background: var(--lime);

  &__box {
    display: grid;
    grid-gap: 12px;
    padding: 48px 0;

    @include mq($bp-medium) {
      grid-gap: 16px;
      grid-template-columns: minmax(300px, 524px) minmax(600px, 1fr);
      padding: 80px 0;
    }
  }

  &__content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 32px 24px 0;
    color: var(--blackMain);
    background-color: #8FD212;
    background-image: url('@/assets/images/landing/form/balls.png');
    background-repeat: no-repeat;
    background-position: calc(100% - 8px) -10px;
    background-size: 80px;
    border-radius: 12px;

    @include mq($bp-small) {
      padding: 48px 40px 0;
      border-radius: 20px;
      background-position: calc(100% - 20px) 0%;
      background-size: auto;
    }
  }

  &__image {
    max-width: 80px;

    @include mq($bp-small-medium) {
      max-width: 100%;
    }
  }

  &__title {
    margin-bottom: 12px;
    font-weight: 600;
    font-size: 22px;
    line-height: 26px;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 30px;
    }
  }

  &__text {
    @include text_normal;

    max-width: 100%;
    margin-bottom: 28px;

    @include mq($bp-small-medium) {
      max-width: 420px;
    }

    @include mq($bp-small) {
      margin-bottom: 76px;
    }
  }

  &__form {
    display: flex;
    flex-direction: column;
    padding: 32px 24px 24px;
    color: var(--blackMain);
    background: var(--white);
    border-radius: 12px;

    @include mq($bp-small) {
      padding: 48px 60px;
      border-radius: 20px;
    }
  }

  &__rows {
    display: grid;
    grid-gap: 16px;

    @include mq($bp-small-medium) {
      grid-gap: 20px;
    }
  }

  &__row {
    display: grid;
    grid-gap: 16px;

    @include mq($bp-small-medium) {
      grid-gap: 20px;
    }

    &--double {
      @include mq($bp-small-medium) {
        grid-template-columns: repeat(2, 1fr);
      }
    }
  }

  &__btn {
    margin-top: 28px;
    height: 44px;

    @include mq($bp-small-medium) {
      margin-top: 32px;
    }

    @include mq($bp-medium) {
      height: 56px;
    }
  }

  &__note {
    margin-top: 8px;
    color: var(--grayBlack);
    font-size: 10px;
    line-height: 14px;
    text-align: center;

    @include mq($bp-small) {
      font-size: 12px;
      line-height: 16px;
      text-align: left;
    }

    a {
      color: var(--blackMain);
      text-decoration: underline;
    }
  }
}
</style>
