<template>
  <div class="fint-item-video">
    <div class="fint-item-video__content">
      <p class="fint-item-video__title">
        Видео о<br>функциях<br>сервиса
      </p>

      <a
        href="#"
        class="fint-item-video__btn"
        @click.prevent
      >
        <UIBaseIcon name="landing/icon-play" />
      </a>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.fint-item-video {
  height: 198px;
  padding: 24px 20px 12px;
  background-color: var(--blackMain);
  background-image: url('@/assets/images/landing/find-item/video-preview.png');
  background-repeat: no-repeat;
  background-position: 100% calc(100% - 12px);
  background-size: 190px;
  border-radius: 8px;
  overflow: hidden;

  @include mq($bp-small-medium) {
    height: 300px;
    background-size: 290px;
  }

  @include mq($bp-small) {
    height: 400px;
    padding: 48px 48px 40px;
    background-position: 100% calc(100% - 22px);
    background-size: auto;
    border-radius: 20px;
  }

  @include mq($bp-medium) {
    height: auto;
  }

  &__content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-between;
    height: 100%;
  }

  &__title {
    color: var(--white);
    font-weight: 500;
    font-size: 15px;
    line-height: 20px;

    @include mq($bp-small) {
      font-size: 32px;
      line-height: 38px;
    }
  }

  &__btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    padding-left: 5px;
    border: 1px solid var(--white);
    border-radius: 50%;

    @include mq($bp-small) {
      width: 64px;
      height: 64px;
    }
  }
}
</style>
