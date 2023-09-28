<template>
  <div class="item-lk">
    <template v-if="!isLoading">
      <div class="container-lk">
        <div class="item-lk__box">
          <LkGoBack
            link="/lk"
            text="Вернуться к товарам"
            class="item-lk__back"
          />

          <div
            v-if="info"
            class="item-lk__card item-lk-card"
          >
            <div class="item-lk-card__header">
              <a
                href="/"
                target="_blank"
                class="item-lk-card__link"
              >
                {{ info.name }}
                <UIBaseIcon name="lk/icon-share" />
              </a>
              <div class="item-lk-card__stats">
                <div class="item-lk-card__stat item-lk-card-stat">
                  <span class="item-lk-card-stat__stars">
                    <UIBaseIcon
                      v-for="i in 5"
                      :key="i"
                      name="lk/icon-star"
                    />
                  </span>
                  <span class="item-lk-card-stat__label">
                    {{ info.rating }}
                    <small>
                      ({{ info.feedbacks }} {{ declOfNum(info.feedbacks, ['отзыв', 'отзыва', 'отзывов']) }})
                    </small>
                  </span>
                </div>

                <button
                  type="button"
                  class="item-lk-card__stat item-lk-card-stat"
                  @click.prevent="copyText(info.articul)"
                >
                  <UIBaseIcon
                    name="lk/icon-wb"
                    class="item-lk-card-stat__icon"
                  />
                  <span class="item-lk-card-stat__label">
                    Артикул:
                  </span>
                  {{ info.articul }}
                  <UIBaseIcon name="lk/icon-copy" />
                </button>

                <div class="item-lk-card__stat item-lk-card-stat">
                  <span class="item-lk-card-stat__label">
                    Добавлено:
                  </span>
                  {{ dateFormat(info.created_at) }}
                </div>
              </div>
            </div>
            <div class="item-lk-card__body">
              <div class="item-lk-card__image">
                <img
                  v-lazy-load
                  :data-src="getProductUrl(info.articul)"
                  alt=""
                >
              </div>
              <div class="item-lk-card__list">
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Основная категория
                  </p>
                  <NuxtLink
                    v-for="(item, i) in info.categories"
                    :key="i"
                    :to="`/lk/category`"
                    class="item-lk-card__value item-lk-card__value--link"
                  >
                    {{ item.name }}
                    <UIBaseIcon
                      name="lk/icon-arrow-left"
                      class="item-lk-card__arrow"
                    />
                  </NuxtLink>
                </div>
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Бренд
                  </p>
                  <NuxtLink
                    :to="`/lk/brand/${info.brand_id}`"
                    class="item-lk-card__value item-lk-card__value--link"
                  >
                    {{ info.brand }}
                  </NuxtLink>
                </div>
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Продавец
                  </p>
                  <NuxtLink
                    :to="`/lk/seller/${info.supplier_id}`"
                    class="item-lk-card__value item-lk-card__value--link"
                  >
                    <!-- ИП Сельская Дарья (320774600299021) -->
                    --
                  </NuxtLink>
                </div>
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Цена
                  </p>
                  <p class="item-lk-card__value">
                    {{ info?.priceU.toLocaleString() || 0 }} ₽
                  </p>
                </div>
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Скидка
                  </p>
                  <p class="item-lk-card__value">
                    {{ parseInt(100 - info.price / (info.priceU / 100)) }} %
                  </p>
                </div>
                <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Сумма продажи
                  </p>
                  <p class="item-lk-card__value">
                    {{ info?.price.toLocaleString() || 0 }} ₽
                  </p>
                </div>
                <!-- <div class="item-lk-card__row">
                  <p class="item-lk-card__label">
                    Персональная скидка
                  </p>
                  <p class="item-lk-card__value">
                    24 %
                  </p>
                </div> -->
              </div>
            </div>
          </div>

          <div class="item-lk__info">
            <LkTableTypes />

            <LkTableDate />
          </div>

          <div class="item-lk__graphics">
            <div class="item-lk-graphic">
              <p class="item-lk-graphic__title">
                Цена и оборот
              </p>
              <div class="item-lk-graphic__badges">
                <span class="badge badge--orange">
                  Цена:
                  <span class="badge__value">
                    866 ₽
                  </span>
                </span>
                <span class="badge badge--purple">
                  Оборот по продажам:
                  <span class="badge__value">
                    10 425 866 ₽
                  </span>
                </span>
                <span class="badge badge--blue">
                  Оборот по заказам::
                  <span class="badge__value">
                    10 425 866 ₽
                  </span>
                </span>
                <span class="badge">
                  Оборот по счетчику WB:
                  <span class="badge__value">
                    8 425 866 ₽
                  </span>
                </span>
              </div>
              <div class="item-lk-graphic__chart">
                <LkChart
                  :data="data1"
                  :options="options"
                />
              </div>
            </div>

            <div class="item-lk-graphic">
              <p class="item-lk-graphic__title">
                Скидки
              </p>
              <div class="item-lk-graphic__badges">
                <span class="badge badge--green">
                  Скидка:
                  <span class="badge__value">
                    75,9%
                  </span>
                </span>
                <span class="badge badge--yellow">
                  Персональная скидка:
                  <span class="badge__value">
                    24%
                  </span>
                </span>
              </div>
              <div class="item-lk-graphic__chart">
                <LkChart
                  :data="data2"
                  :options="options"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div
      v-else
      class="item-lk__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
import { format } from 'date-fns'

import copyTextToClipboard from '@/utils/copyTextToClipboard.js'
import GenerateImgUrl from '@/utils/generateImgUrl.js'
import declOfNum from '@/utils/declOfNum.js'

definePageMeta({
  layout: 'lk',
})

const route = useRoute()

const { slug } = route.params
const isLoading = ref(false)
const info = ref(null)

const copyText = async (text) => {
  await copyTextToClipboard(text)
}

const dateFormat = (date) => {
  return format(new Date(date * 1000), 'dd.MM.yyyy')
}

const getProductUrl = (id) => {
  return new GenerateImgUrl(id, 'big').url()
}

const data1 = {
  labels: [],
  datasets: [
    {
      label: 'Оборот по заказам',
      valueSuffix: '₽',
      borderColor: '#5480F2',
      pointBorderColor: '#5480F2',
      data: [],
    },
    {
      label: 'Оборот по продажам',
      valueSuffix: '₽',
      borderColor: '#AE80EA',
      pointBorderColor: '#AE80EA',
      data: [],
    },
    {
      label: 'Средний чек',
      valueSuffix: '₽',
      borderColor: '#FF8F6D',
      pointBorderColor: '#FF8F6D',
      data: [],
    },
  ],
}

const data2 = {
  labels: [],
  datasets: [
    {
      label: 'Остатки',
      valueSuffix: 'шт.',
      borderColor: '#22A873',
      pointBorderColor: '#22A873',
      data: [],
    },
    {
      label: 'Возвраты и поставки',
      valueSuffix: 'шт.',
      borderColor: '#98D920',
      pointBorderColor: '#98D920',
      data: [],
    },
  ],
}

const options = {}

const setDefault1 = () => {
  const labels = []
  for (let i = 10; i <= 28; i++) {
    labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
  }
  data1.labels = labels

  const values1 = []
  const values2 = []
  const values3 = []

  for (let i = 0; i <= 18; i++) {
    values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
    values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
    values3.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
  }
  data1.datasets[0].data = values1
  data1.datasets[1].data = values2
  data1.datasets[2].data = values3
}

const setDefault2 = () => {
  const labels = []
  for (let i = 10; i <= 28; i++) {
    labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
  }
  data2.labels = labels

  const values1 = []
  const values2 = []

  for (let i = 0; i <= 18; i++) {
    values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
    values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
  }
  data2.datasets[0].data = values1
  data2.datasets[1].data = values2
}

setDefault1()
setDefault2()

const getItem = async () => {
  if (!slug) {
    return navigateTo('/lk')
  }

  isLoading.value = true
  const { data } = await useFetch(`/api/products/${slug}`, {
    watch: false,
  })
  isLoading.value = false

  info.value = data?.value || null
}

await getItem()
</script>

<style lang="scss" scoped>
@import '@/assets/styles/components/badge.scss';

.item-lk {
  &__box {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 24px 0 100px;
  }

  &__back {
    margin-bottom: 20px;
  }

  &__card {
    margin-bottom: 60px;
  }

  &__info {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
    margin-bottom: 32px;
  }

  &__graphics {
    width: 100%;
    display: grid;
    grid-gap: 60px;
    padding: 24px 40px 40px;
    background: var(--white);
    border-radius: 16px;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 100px auto;
  }
}

.item-lk-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 28px 40px 48px;
  background: var(--white);
  border-radius: 16px;

  &__header {
    display: flex;
    flex-direction: column;
    padding-bottom: 20px;
    border-bottom: 1px solid #E2E2E7;
  }

  &__link {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 12px;
    font-weight: 600;
    font-size: 24px;
    line-height: 32px;
  }

  &__stats {
    display: grid;
    grid-gap: 16px;
    grid-template-columns: repeat(3, auto);
    justify-content: flex-start;
    align-items: center;
  }

  &__body {
    display: grid;
    grid-gap: 60px;
    grid-template-columns: 300px 1fr;
    padding-top: 32px;
  }

  &__list {
    display: flex;
    flex-direction: column;
  }

  &__row {
    display: flex;
    align-items: center;
    padding: 20px;

    &:nth-child(odd) {
      background: #F8F8F9;
    }
  }

  &__label {
    width: 240px;
    font-size: 14px;
    line-height: 18px;
  }

  &__value {
    display: flex;
    align-items: center;
    font-weight: 500;
    font-size: 16px;
    line-height: 20px;

    &--link {
      color: #33976F;
      font-size: 14px;
      line-height: 18px;

      ::v-deep(.ui-icon) {
        svg path {
          fill: #33976F;
        }
      }
    }

    &:last-child {
      .item-lk-card__arrow {
        display: none;
      }
    }
  }

  &__arrow {
    margin: 0 4px;
    transform: rotate(180deg);
  }
}

.item-lk-card-stat {
  display: grid;
  grid-gap: 4px;
  grid-template-columns: repeat(4, auto);
  align-items: center;
  justify-content: flex-start;
  font-size: 16px;
  line-height: 20px;

  &__stars {
    display: flex;
    align-items: center;

    ::v-deep(.ui-icon) {
      width: 16px;
      height: 16px;

      svg path {
        fill: #F2CF3A;
      }
    }
  }

  &__icon {
    margin-right: 2px;
  }

  &__label {
    display: flex;
    align-items: center;
    font-weight: 500;

    small {
      margin-left: 4px;
      font-weight: 400;
      font-size: 14px;
      line-height: 18px;
      color: #8B8B91;
    }
  }
}

.item-lk-graphic {
  display: flex;
  flex-direction: column;

  &__title {
    margin-bottom: 16px;
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__badges {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin: -4px;

    .badge {
      margin: 4px;
    }
  }

  &__chart {
    width: 100%;
    height: 420px;
    margin-top: 32px;
  }
}
</style>
