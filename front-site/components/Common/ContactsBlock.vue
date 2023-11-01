<template>
  <div :class="['contacts-block', { 'contacts-block--gray' : primaryGray }]">
    <div class="contacts-block__content">
      <p class="contacts-block__title">
        {{ title || 'Мы на связи' }}
      </p>

      <p class="contacts-block__text">
        Если у вас возникли вопросы или вы хотите поделиться своим опытом, напишите нам на почту или в телеграмм.
        <br>
        Мы свяжемся в течение 24 часов.
      </p>
    </div>

    <div class="contacts-block__cards">
      <div class="contacts-block__card">
        <p class="contacts-block__label">
          Электронная почта
        </p>
        <a
          href="mailto:support@spotter.fun"
          target="_blank"
          rel="nofollow"
          class="contacts-block__value"
        >
          support@spotter.fun
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  primaryGray: {
    type: Boolean,
    default: false,
  },
})
</script>

<style lang="scss" scoped>
.contacts-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 32px 24px 24px;
  background: var(--white);
  border-radius: 12px;

  @include mq($bp-medium) {
    flex-direction: row;
    align-items: center;
    padding: 48px 56px;
    border-radius: 20px;
  }

    &--gray {
      color: var(--blackMain);
      background: #F3F4F5;
    }

  &__content {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 480px;
    margin-bottom: 32px;

    @include mq($bp-medium) {
      margin-bottom: 0;
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
  }

  &__cards {
    display: grid;
    grid-gap: 8px;
    width: 100%;

    @include mq($bp-small-medium) {
      width: auto;
      grid-gap: 12px;
      grid-template-columns: repeat(1, minmax(220px, 260px));
    }
  }

  &__card {
    width: 100%;
    max-width: 260px;
    display: flex;
    flex-direction: column;
    padding: 16px 20px;
    background: var(--lime);
    border-radius: 8px;

    @include mq($bp-small) {
      padding: 24px;
      border-radius: 12px;
    }
  }

  &__label {
    margin-bottom: 2px;
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small) {
      margin-bottom: 4px;
      font-size: 14px;
    }
  }

  &__value {
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;

    @include mq($bp-small) {
      font-size: 20px;
    }
  }
}
</style>
