<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="success-sign-up">
      <p class="success-sign-up__title">
        Вы успешно зарегистрировались
      </p>

      <div class="success-sign-up__body">
        <div class="success-sign-up__icon">
          <UIBaseIcon name="landing/icon-galka" />
        </div>

        <p class="success-sign-up__text">
          Чтобы вы не забыли данные для входа, мы отправили их на ваш e-mail
        </p>

        <UIBaseButton
          text="Хорошо"
          full-width
          primary-black-outline
          class="success-sign-up__btn"
          @click="closeModal()"
        />
      </div>
    </div>
  </ModalsLayout>
</template>

<script setup>
const emits = defineEmits(['close'])

const closeModal = () => {
  emits('close')
}
</script>

<style lang="scss" scoped>
.success-sign-up {
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

    margin-bottom: 20px;
    text-align: center;

    @include mq($bp-small) {
      margin-bottom: 48px;
    }
  }

  &__body {
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

  &__btn {
    max-width: 200px;
    margin-top: 30px;
    padding: 13px 0;

    @include mq($bp-small) {
      margin-top: 56px;
      padding: 20px 0;
    }
  }
}
</style>
