<template>
  <div class="what-else">
    <div class="container">
      <div class="what-else__box">
        <h2 class="what-else__title">
          Как еще пользоваться сервисом
        </h2>

        <p class="what-else__text">
          Наша задача – помогать вам зарабатывать.
          <br>
          Присоединяйтесь, а мы сделаем все возможное для вашего роста.
        </p>

        <Swiper
          :slides-per-view="'auto'"
          :space-between="12"
          :breakpoints="{
            '768': {
              spaceBetween: 16
            }
          }"
          class="what-else__cards"
        >
          <SwiperSlide class="what-else__card what-else-card">
            <p class="what-else-card__title">
              Следите за своей нишей. Данные по всем товарам обновляются ежедневно
            </p>
            <UIBaseButton text="Начать анализ" primary-white-outline class="what-else-card__btn" />
          </SwiperSlide>
          <SwiperSlide class="what-else__card what-else-card what-else-card_2">
            <p class="what-else-card__title">
              Проверяйте гипотезы
            </p>
            <UIBaseButton text="Попробовать" primary-white-outline class="what-else-card__btn" />
          </SwiperSlide>
          <SwiperSlide class="what-else__card what-else-card what-else-card_3">
            <p class="what-else-card__title">
              Анализируйте конкурентов
            </p>
            <UIBaseButton text="Попробовать" primary-black-outline class="what-else-card__btn" />
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.what-else {
  &__box {
    display: flex;
    flex-direction: column;
    padding: 60px 0;

    @include mq($bp-medium) {
      padding: 100px 0;
    }
  }

  &__title {
    @include h2;

    margin-bottom: 8px;
    color: var(--blackMain);
    text-align: center;
  }

  &__text {
    max-width: 720px;
    margin: 0 auto 28px;
    color: var(--grayBlack);
    font-size: 13px;
    line-height: 18px;
    text-align: center;

    @include mq($bp-small) {
      margin: 0 auto 40px;
      font-size: 18px;
      line-height: 26px;
    }
  }

  &__cards {
    width: calc(100% + 40px);
    margin: 0 -20px;
    padding: 0px 20px;

    @include mq($bp-small) {
      width: calc(100% + 60px);
      margin: 0 -30px;
      padding: 0px 30px;
    }
  }

  &__card {
    max-width: 280px;

    @include mq($bp-small) {
      max-width: 416px;
    }
  }
}

.what-else-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  height: 340px;
  padding: 24px 20px 20px;
  color: var(--white);
  background: var(--blackMain);
  border-radius: 24px;
  overflow: hidden;

  @include mq($bp-small) {
    height: 460px;
    padding: 40px 32px 32px;
  }

  &:before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-image: url('@/assets/icons/landing/what-else/1.svg');
    background-repeat: no-repeat;
    background-position: calc(100% + 3px) calc(100% - 79px);
    background-size: 276px;

    @include mq($bp-small) {
      background-position: calc(100% - 6px) calc(100% - 77px);
      background-size: auto;
    }
  }

  &_2 {
    background-color: var(--purple);

    &:before {
      background-image: url('@/assets/icons/landing/what-else/2.svg');
      background-position: calc(100% + 17px) calc(100% - 55px);
      background-size: 277px;

      @include mq($bp-small) {
        background-position: 100% calc(100% - 56px);
        background-size: auto;
      }
    }
  }

  &_3 {
    color: var(--blackMain);
    background-color: #F3F4F5;

    &:before {
      background-image: url('@/assets/icons/landing/what-else/3.svg');
      background-position: -10px 100%;
      background-size: 397px 284px;

      @include mq($bp-small) {
        background-position: 100% 100%;
        background-size: auto;
      }
    }
  }

  &__title {
    font-weight: 500;
    font-size: 15px;
    line-height: 20px;
    z-index: 1;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 32px;
    }
  }

  &__btn {
    font-size: 13px;
    line-height: 16px;
    padding: 12px 24px;

    @include mq($bp-small) {
      padding: 14px 38px;
      font-size: 16px;
      line-height: 22px;
    }
  }
}
</style>
