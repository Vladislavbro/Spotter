<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="cancel-subscribe">
      <p class="cancel-subscribe__title">
        Отмена подписки
      </p>

      <div class="cancel-subscribe__box">
        <p class="cancel-subscribe__text">
          Вы уверены, что хотите отменить подписку? Вы потеряете доступ к сервису, как только отмените подписку.
        </p>

        <div class="cancel-subscribe__btns">
          <UILkButton
            text="Убрать подписку"
            is-big
            class="cancel-subscribe__btn"
            @click="closeModal()"
          />

          <UILkButton
            text="Оставить подписку"
            primary-gray
            is-big
            class="cancel-subscribe__btn"
            @click="closeModal()"
          />
        </div>
      </div>
    </div>
  </ModalsLayout>
</template>

<script setup>
const emits = defineEmits(['close', 'success'])

const closeModal = () => {
  emits('close')
}
</script>

<style lang="scss" scoped>
.cancel-subscribe {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 740px;
  padding: 40px 110px 48px;
  color: var(--blackMain);
  background: #FFFFFF;
  border-radius: 16px;

  &__title {
    @include h4;

    margin-bottom: 24px;
    text-align: center;
  }

  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  &__text {
    @include text_normal;

    margin-bottom: 48px;
  }

  &__btns {
    display: grid;
    grid-template-columns: repeat(2, 200px);
    grid-gap: 12px;
  }
}
</style>
