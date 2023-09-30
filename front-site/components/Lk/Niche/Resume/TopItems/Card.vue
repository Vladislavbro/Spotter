<template>
  <NuxtLink
    :to="`/lk/item/${item.product__articul}`"
    class="top-items-card"
  >
    <div class="top-items-card__image">
      <img
        v-lazy-load
        :data-src="getProductUrl(item.product__articul)"
        alt=""
      >
    </div>
    <p class="top-items-card__reviews">
      <span class="top-items-card__icon">
        <UIBaseIcon name="lk/icon-star" />
      </span>
      {{ item.product__rating }}
      <span>
        ({{ item.product__feedbacks }} {{ declOfNum(item.product__feedbacks, ['отзыв', 'отзыва', 'отзывов']) }})
      </span>
    </p>
    <p class="top-items-card__title">
      {{ item.product__name }}
    </p>
    <p class="top-items-card__label">
      Оборот товара
    </p>
    <p class="top-items-card__value">
      {{ item?.[`profit_${day}_${type}`]?.toLocaleString() || 0 }} ₽
      <!-- <span class="top-items-card__percent">
        +2.2%
      </span> -->
    </p>
  </NuxtLink>
</template>

<script setup>
import GenerateImgUrl from '@/utils/generateImgUrl.js'
import declOfNum from '@/utils/declOfNum.js'

defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  type: {
    type: String,
    default: 'fbo',
  },
  day: {
    type: Number,
    default: 30,
  },
})

const getProductUrl = (id) => {
  return new GenerateImgUrl(id).url()
}
</script>

<style lang="scss" scoped>
.top-items-card {
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  background: var(--white);
  border-radius: 12px;

  &__image {
    width: 140px;
    height: 180px;
    margin: 0 auto 20px;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__reviews {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(3, auto);
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 4px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;

    span {
      color: #8B8B91;
      font-weight: 400;
      font-size: 13px;
    }
  }

  &__icon {
    ::v-deep(.ui-icon) {
      svg {
        width: 16px;
        height: 16px;
      }

      svg path {
        fill: #F2CF3A;
      }
    }
  }

  &__title {
    margin-bottom: 20px;
    font-size: 15px;
    line-height: 18px;
  }

  &__label {
    margin-bottom: 6px;
    color: #8B8B91;
    font-size: 13px;
    line-height: 16px;
  }

  &__value {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: flex-start;
    font-weight: 500;
    font-size: 20px;
    line-height: 24px;
  }

  &__percent {
    font-size: 13px;
    line-height: 16px;
    color: #09A668;
  }
}
</style>
