<template>
  <div id="reviews" class="reviews">
    <div class="container">
      <div class="reviews__box">
        <div class="reviews__header">
          <div class="reviews__left">
            <h2 class="reviews__title">
              Отзывы
            </h2>

            <div class="reviews__rating">
              <div class="reviews__stars">
                <UIBaseIcon
                  v-for="i in 5"
                  :key="i"
                  name="landing/icon-star"
                />
              </div>
              <p class="reviews__rating-count">
                4.9
              </p>
            </div>
          </div>

          <div class="reviews__arrows">
            <button class="reviews__arrow reviews__arrow_left">
              <UIBaseIcon name="landing/icon-arrow-left" />
            </button>
            <button class="reviews__arrow reviews__arrow_right">
              <UIBaseIcon name="landing/icon-arrow-left" />
            </button>
          </div>
        </div>

        <Swiper
          :modules="[SwiperNavigation]"
          :slides-per-view="'auto'"
          :space-between="12"
          :navigation="{
            nextEl: '.reviews__arrow_right',
            prevEl: '.reviews__arrow_left',
          }"
          loop
          :breakpoints="{
            '1181': {
              slidesPerView: 3,
              spaceBetween: 16
            },
            '992': {
              slidesPerView: 2,
              spaceBetween: 16
            },
            '0': {
              slidesPerView: 'auto',
              spaceBetween: 12
            }
          }"
          class="reviews__slider"
        >
          <SwiperSlide
            v-for="(item, i) in cards"
            :key="i"
            class="reviews__slide"
          >
            <LandingReviewsCard
              :item="item"
            />
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  </div>
</template>

<script setup>
import imgUrl1 from '@/assets/images/landing/reviews/1.png'
import imgUrl2 from '@/assets/images/landing/reviews/2.png'
import imgUrl3 from '@/assets/images/landing/reviews/3.png'

const cards = [
  {
    image: imgUrl1,
    name: 'Кирилл',
    date: '6 июля 2023',
    rating: 5,
    text: 'Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром',
  },
  {
    image: imgUrl2,
    name: 'Александра',
    date: '22 февраля 2023',
    rating: 4,
    text: 'За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз. За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз. За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз.',
  },
  {
    image: imgUrl3,
    name: 'Константин',
    date: '1 декабря 2022',
    rating: 5,
    text: 'Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж.',
  },
  {
    image: imgUrl1,
    name: 'Кирилл',
    date: '6 июля 2023',
    rating: 5,
    text: 'Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром',
  },
  {
    image: imgUrl2,
    name: 'Александра',
    date: '22 февраля 2023',
    rating: 4,
    text: 'За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз. За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз. За полгода полностью поменяла нишевание на Wildberries и увеличила доход в 5 раз.',
  },
  {
    image: imgUrl3,
    name: 'Константин',
    date: '1 декабря 2022',
    rating: 5,
    text: 'Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж. Оборот  может служить ориентиром для ваших продаж.',
  },
]
</script>

<style lang="scss" scoped>
.reviews {
  &__box {
    display: flex;
    flex-direction: column;
    padding: 60px 0;
    color: var(--blackMain);

    @include mq($bp-medium) {
      padding: 100px 0;
    }
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 28px;

    @include mq($bp-small-medium) {
      justify-content: space-between;
      margin-bottom: 40px;
    }
  }

  &__left {
    display: flex;
    align-items: center;
    flex-direction: column;

    @include mq($bp-small-medium) {
      flex-direction: row
    }
  }

  &__title {
    @include h2;

    margin-bottom: 4px;

    @include mq($bp-small-medium) {
      margin-bottom: 0;
    }
  }

  &__rating {
    display: flex;
    align-items: center;

    @include mq($bp-small-medium) {
      margin-left: 16px;
    }
  }

  &__stars {
    display: flex;
    align-items: center;
  }

  &__rating-count {
    margin-left: 4px;
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;

    @include mq($bp-small) {
      margin-left: 8px;
      font-size: 24px;
      line-height: 28px;
    }
  }

  &__arrows {
    display: none;

    @include mq($bp-small-medium) {
      display: grid;
      grid-gap: 8px;
      grid-template-columns: repeat(2, auto);
    }
  }

  &__arrow {
    &_right {
      transform: rotate(180deg);
    }
  }

  &__slider {
    width: calc(100% + 40px);
    margin: 0 -20px;
    padding: 1px 20px;
    overflow: hidden;

    @include mq($bp-small-medium) {
      width: 100%;
      margin: 0;
      padding: 0;
    }
  }

  &__slide {
    max-width: 260px;

    @include mq($bp-small-medium) {
      max-width: 350px;
    }

    @include mq($bp-medium) {
      max-width: 100%;
    }
  }
}
</style>
