<template>
  <div class="more-info">
    <div class="container">
      <div class="more-info__box">
        <div class="more-info__avatars">
          <img src="@/assets/images/landing/more-info/1.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/2.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/3.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/4.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/5.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/6.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/7.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/8.jpg" class="more-info__avatar">
          <img src="@/assets/images/landing/more-info/9.jpg" class="more-info__avatar">
        </div>

        <p class="more-info__title">
          <span>Spotter</span> помогает и приносит прибыль нашим пользователям
        </p>

        <p class="more-info__text">
          Сервис только начинает развиваться, его функционал будет пополняться. Сейчас это идеальная площадка для выбора правильной ниши за минимальную плату.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.more-info {
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

  &__avatars {
    display: flex;
    align-items: center;
    margin-bottom: 20px;

    @include mq($bp-small) {
      margin-bottom: 28px;
    }
  }

  &__avatar {
    width: 48px;
    height: 48px;
    margin-left: -12px;
    border-radius: 50%;
    overflow: hidden;

    @include mq($bp-small) {
      width: 64px;
      height: 64px;
    }

    &:first-child {
      margin-left: 0;
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__title {
    margin-bottom: 12px;
    font-size: 18px;
    line-height: 24px;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 30px;
    }

    span {
      color: var(--lime);
    }
  }

  &__text {
    @include text_normal;

    max-width: 650px;
    color: var(--grayLight);
  }
}
</style>
