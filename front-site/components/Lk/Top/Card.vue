<template>
  <div class="top-card">
    <div class="top-card__box">
      <NuxtLink
        :to="link"
        class="top-card__image"
      >
        <img
          v-if="item.product_articul"
          v-lazy-load
          :data-src="getProductUrl(item.product_articul)"
          alt=""
        >
      </NuxtLink>

      <div class="top-card__content">
        <NuxtLink
          :to="link"
          class="top-card__name"
        >
          {{ item.name }}
        </NuxtLink>

        <div class="top-card__bottom">
          <div
            :class="[
              'perspective perspective--bad',
              { 'perspective--bad' : scoring <= 5 },
              { 'perspective--normal' : scoring > 5 && scoring <= 10 },
              { 'perspective--good' : scoring > 10 },
            ]"
          >
            <p class="perspective__label">
              Перспективность ниши
              <span class="perspective__point">
                {{ scoring }}/15
              </span>
            </p>
            <div class="perspective__bar">
              <div
                :style="`width: ${100 / 15 * scoring}%`"
                class="perspective__progress"
              />
            </div>
          </div>

          <NuxtLink
            :to="link"
            class="top-card__link"
          >
            Товары и аналитика
          </NuxtLink>
        </div>
      </div>
    </div>

    <div class="top-card__info">
      <div class="top-card__line">
        <p class="top-card__label">
          Объем рынка:
        </p>
        <p class="top-card__value">
          {{ item?.scoring?.profit?.toLocaleString() || 0 }} ₽
        </p>
      </div>
      <!-- <div class="top-card__line">
        <p class="top-card__label">
          Ценовой сегмент:
        </p>
        <p class="top-card__value">
          0
        </p>
      </div> -->
      <div class="top-card__line">
        <p class="top-card__label">
          Средний чек:
        </p>
        <p class="top-card__value">
          {{ item?.price_avg?.toLocaleString() || 0 }} ₽
        </p>
      </div>
      <div class="top-card__line">
        <p class="top-card__label">
          Товаров с продажами:
        </p>
        <p class="top-card__value">
          {{ productsSoldedPercent }} %
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import GenerateImgUrl from '@/utils/generateImgUrl.js'

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})

// <!-- Computed -->
const link = computed(() => {
  return `/lk/niche/${props.item?.name?.toLowerCase()}?id=${props.item?.id}`
})

const scoring = computed(() => {
  return props.item?.scoring?.scoring || 0
})

const productsSoldedPercent = computed(() => {
  const productsCount = props.item?.products_count || 0
  const productsSolded = props.item?.products_solded || 0

  return parseInt((productsSolded / productsCount * 100) * 100) / 100
})

// <!-- Methods -->
const getProductUrl = (id) => {
  return new GenerateImgUrl(id).url()
}
</script>

<style lang="scss" scoped>
.top-card {
  display: flex;
  flex-direction: column;
  background: var(--white);
  border-radius: 8px;

  &__box {
    display: flex;
    grid-gap: 20px;

    padding: 20px;
  }

  &__image {
    flex: 0 0 auto;

    width: 120px;
    height: 154px;

    background: #F3F4F5;
    border-radius: 8px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    flex: 1 1 auto;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  &__name {
    font-weight: 600;
    line-height: 20px;
  }

  &__link {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: 40px;

    font-weight: 500;
    font-size: 13px;
    line-height: 16px;

    background: #F3F4F5;
    border-radius: 8px;
  }

  &__bottom {
    display: grid;
    grid-gap: 20px;
  }

  &__info {
    display: grid;
    grid-gap: 12px;
    padding: 16px 20px 20px 20px;
  }

  &__line {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    align-items: center;
    justify-content: flex-start;

    font-size: 13px;
    line-height: 16px;
  }

  &__label {
    font-weight: 500;
  }
}

.perspective {
  display: grid;
  grid-gap: 6px;

  &--bad {
    .perspective {
      &__point {
        color: #DA3434;
        background: #F8D6D6;
      }

      &__bar {
        background: rgba(218, 52, 52, 0.20);
      }

      &__progress {
        background: linear-gradient(270deg, #D93333 0%, #E15441 100%);
      }
    }
  }

  &--normal {
    .perspective {
      &__point {
        color: #F0AB24;
        background: #FFEDCB;
      }

      &__bar {
        background: rgba(255, 196, 82, 0.30);
      }

      &__progress {
        background: linear-gradient(270deg, #FEC351 0%, #F9C748 100%);
      }
    }
  }

  &--good {
    .perspective {
      &__point {
        color: #06986B;
        background: #D5EFE4;
      }

      &__bar {
        background: rgba(45, 174, 119, 0.20);
      }

      &__progress {
        background: linear-gradient(270deg, #05976A 0%, #3FB97C 100%);
      }
    }
  }

  &__label {
    display: flex;
    align-items: center;
    justify-content: space-between;

    font-size: 13px;
    line-height: 16px;
  }

  &__point {
    display: flex;
    align-items: center;
    justify-content: center;

    height: 20px;

    padding: 0px 8px;

    font-weight: 500;

    border-radius: 60px;
  }

  &__bar {
    position: relative;

    width: 100%;
    height: 8px;

    border-radius: 60px;
  }

  &__progress {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;

    border-radius: 60px;
  }
}
</style>
