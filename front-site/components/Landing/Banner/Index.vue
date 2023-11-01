<template>
  <div class="banner">
    <div class="container">
      <div class="banner__box">
        <div class="banner__content">
          <h1 class="banner__title">
            Подборка <span>свободных</span> ниш на Wildberries
          </h1>

          <p class="banner__text">
            Spotter - это сервис для поиска прибыльных товаров
          </p>

          <UIBaseButton
            text="Попробовать бесплатно"
            to="/lk"
            primary-green
            big
            class="banner__btn"
          />

          <p class="banner__note">
            Весь функционал бесплатно на 5 дней.
            <br>
            Без привязки карты.
          </p>
        </div>

        <div class="banner__image">
          <UIBaseIcon name="landing/icon-banner" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.banner {
  background: var(--blackMain);
  overflow: hidden;

  &__box {
    display: grid;
    grid-gap: 40px;
    align-items: center;
    justify-content: center;
    padding: 40px 0 60px;

    @include mq($bp-medium) {
      justify-content: space-between;
      grid-template-columns: minmax(400px, 580px) auto;
      padding: 124px 0 156px;
    }
  }

  &__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 320px;
    margin: 0 auto;
    text-align: center;

    @include mq($bp-small) {
      max-width: 580px;
    }

    @include mq($bp-medium) {
      align-items: flex-start;
      text-align: left;
    }
  }

  &__title {
    margin-bottom: 8px;
    font-weight: 500;
    font-size: 28px;
    line-height: 34px;

    @include mq($bp-small) {
      margin-bottom: 26px;
      font-size: 52px;
      line-height: 60px;
    }

    span {
      color: var(--lime);
    }
  }

  &__text {
    margin-bottom: 28px;
    font-size: 15px;
    line-height: 22px;

    @include mq($bp-small) {
      font-size: 18px;
      line-height: 26px;
    }

    @include mq($bp-medium) {
      margin-bottom: 48px;
    }
  }

  &__btn {
    margin-bottom: 8px;

    @include mq($bp-small) {
      margin-bottom: 12px;
    }
  }

  &__note {
    @include text_normal;

    color: var(--grayLight);

    br {
      @include mq($bp-small) {
        display: none;
      }
    }
  }

  &__image {
    ::v-deep(.ui-icon) {
      svg {
        width: 100%;
        height: auto;
        max-width: 320px;

        @include mq($bp-small-medium) {
          min-width: 500px;
          max-width: 633px;
        }
      }
    }
  }
}
</style>
