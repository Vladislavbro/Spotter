<template>
  <div class="feedback">
    <div class="container">
      <div class="feedback__box">
        <p class="feedback__title">
          Если у вас был отрицательный опыт в работе с подобными сервисами – поделитесь с нами
        </p>

        <p class="feedback__text">
          Мы будем рады учесть ошибки конкурентов и создать по-настоящему нужный продукт.
        </p>

        <UIBaseButton
          text="Поделиться обратной связью"
          primary-green
          class="feedback__btn"
        />
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.feedback {
  background: var(--blackMain);

  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px 0;
    text-align: center;

    @include mq($bp-medium) {
      padding: 60px 0;
    }
  }

  &__title {
    max-width: 900px;
    margin-bottom: 12px;
    font-size: 18px;
    line-height: 24px;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 30px;
    }
  }

  &__text {
    @include text_normal;

    margin-bottom: 28px;
    color: var(--grayLight);
  }

  &__btn {
    padding: 14px 24px;

    @include mq($bp-small) {
      padding: 20px 32px;
    }
  }
}
</style>
