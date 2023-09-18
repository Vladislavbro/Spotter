<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="success-change-password">
      <p class="success-change-password__title">
        Пароль успешно изменен!
      </p>

      <div class="success-change-password__box">
        <div class="success-change-password__icon">
          <UIBaseIcon name="landing/icon-galka" />
        </div>

        <p class="success-change-password__text">
          Отправили новые данные для входа на ваш e-mail.
        </p>
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
.success-change-password {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 740px;
  padding: 40px 0px 90px;
  color: var(--blackMain);
  background: #FFFFFF;
  border-radius: 16px;

  &__title {
    @include h4;

    margin-bottom: 48px;
    text-align: center;
  }

  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    border: 1px solid var(--purple);
    border-radius: 50%;

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
