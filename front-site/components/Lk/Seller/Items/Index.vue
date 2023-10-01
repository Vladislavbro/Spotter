<template>
  <div class="seller-items">
    <template v-if="!isLoadingPage">
      <div class="seller-items__info">
        <LkTableDate
          @change="changeDate"
        />
      </div>

      <div class="seller-items__card">
        <div class="seller-items__card-header">
          <div class="seller-items__card-side">
            <LkTableSettings
              :array="headColumns"
            />
          </div>
        </div>

        <LkTable
          v-if="!isLoading"
          :head-columns="headColumns"
          class="seller-items__table seller-items-table"
        >
          <tbody>
            <tr
              v-for="(item, i) in items"
              :key="i"
            >
              <td v-if="headColumns[0].show">
                <div class="seller-items-table-item">
                  <NuxtLink
                    :to="`/lk/item/${item.product__articul}`"
                    class="seller-items-table-item__image"
                  >
                    <img
                      v-lazy-load
                      :data-src="getProductUrl(item.product__articul)"
                      alt=""
                    >
                  </NuxtLink>
                  <div class="seller-items-table-item__info">
                    <NuxtLink
                      :to="`/lk/item/${item.product__articul}`"
                      class="seller-items-table-item__name"
                    >
                      <span class="seller-items-table-item__name-box">
                        {{ item.product__name }}
                      </span>
                      <UIBaseIcon name="lk/icon-share" />
                    </NuxtLink>
                    <button
                      class="seller-items-table-item__article"
                      @click.prevent="copyText(item.product__articul)"
                    >
                      <UIBaseIcon name="lk/icon-wb" />
                      <span>
                        Артикул:
                      </span>
                      {{ item.product__articul }}
                      <UIBaseIcon name="lk/icon-copy" />
                    </button>
                    <p class="seller-items-table-item__rating">
                      <UIBaseIcon name="lk/icon-star" />
                      {{ item.product__rating }}
                      <span class="seller-items-table-item__reviews">
                        ({{ item.product__feedbacks }} {{ declOfNum(item.product__feedbacks, ['отзыв', 'отзыва', 'отзывов']) }})
                      </span>
                    </p>
                  </div>
                </div>
              </td>
              <td v-if="headColumns[1].show">
                <div class="seller-items-table__price">
                  <p class="seller-items-table__newprice">
                    {{ item?.price.toLocaleString() || 0 }} ₽
                    <span class="seller-items-table__price-percent">
                      {{ parseInt(100 - item.price / ( item.priceU / 100 )) }}%
                    </span>
                  </p>
                  <span class="seller-items-table__oldprice">
                    {{ item?.priceU.toLocaleString() || 0 }} ₽
                  </span>
                </div>
              </td>
              <td>
                <NuxtLink
                  :to="`/lk/seller/${item.product__supplier_id}?name=${item?.supplier?.name || ''}&id=${item?.supplier?.wb_id || ''}`"
                  class="seller-items-table__link"
                >
                  {{ item?.supplier?.name || '--' }}
                  <br>
                  {{ item?.supplier?.inn ? `(${item.supplier.inn})` : '' }}
                </NuxtLink>
              </td>
              <td>
                <NuxtLink
                  :to="`/lk/brand/${item.product__brand_id}?name=${item?.product__brand?.toLowerCase() || ''}`"
                  class="seller-items-table__link"
                >
                  {{ item.product__brand }}
                </NuxtLink>
              </td>
              <td v-if="headColumns[2].show">
                <p class="seller-items-table__stats">
                  {{ item[`profit_${day}_fbo`].toLocaleString() || 0 }} ₽
                </p>
              </td>
              <td v-if="headColumns[3].show">
                <p class="seller-items-table__stats">
                  {{ item[`sales_${day}_fbo`].toLocaleString() || 0 }}
                </p>
              </td>
            </tr>
          </tbody>
        </LkTable>

        <div
          v-else
          class="seller-items__loader"
        >
          <UILoader />
        </div>
      </div>
    </template>
    <div
      v-else
      class="seller-items__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
import copyTextToClipboard from '@/utils/copyTextToClipboard.js'
import GenerateImgUrl from '@/utils/generateImgUrl.js'
import declOfNum from '@/utils/declOfNum.js'

const route = useRoute()
const { $toast } = useNuxtApp()

const { slug } = route.params

const headColumns = ref([
  { label: 'Название товара', show: true },
  { label: 'Цена', slug: 'price', sort: true, show: true },
  { label: 'Продавец', show: true },
  { label: 'Бренд', show: true },
  { label: 'Оборот', slug: 'profit_30_fbo', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Продажи, шт.', slug: 'sales_30_fbo', sort: true, show: true },
])

const items = ref([])
const day = ref(30)

const isLoadingPage = ref(true)
const isLoading = ref(false)

const changeDate = (data) => {
  items.value = []
  day.value = data.day

  getData()
}

const copyText = async (text) => {
  try {
    await copyTextToClipboard(text)

    $toast.success('Артикул товара скопирован')
  } catch (e) {
    $toast.success('Не удалось скопировать артикул товара')
  }
}

const getProductUrl = (id) => {
  return new GenerateImgUrl(id).url()
}

const getData = async () => {
  isLoading.value = true

  const { data } = await useFetch(`/api/suppliers/${slug}`, {
    watch: false,
    query: {
      view: 'products',
      period: day.value,
    },
  })

  items.value = data?.value?.items || []

  isLoadingPage.value = false
  isLoading.value = false
}

getData()
</script>

<style lang="scss" scoped>
.seller-items {
  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 100px 0;
  }

  &__info {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
    margin-bottom: 32px;
  }

  &__filter {
    margin-bottom: 32px;
  }

  &__card {
    display: flex;
    flex-direction: column;
    margin-bottom: 40px;
    padding: 24px 20px 20px;
    background: var(--white);
    border-radius: 12px;
  }

  &__card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
  }

  &__card-side {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
  }
}

.seller-items-table {
  &__name {
    display: grid;
    grid-gap: 2px;
  }

  &__price {
    display: grid;
    grid-gap: 4px;
    line-height: 14px;
  }

  &__newprice {
    font-size: 15px;
    line-height: 18px;
  }

  &__price-percent {
    margin-left: 4px;
    padding: 4px 6px;
    font-size: 11px;
    color: #33976F;
    background: #F8F8F9;
    border-radius: 4px;
  }

  &__oldprice {
    font-size: 12px;
    text-decoration-line: line-through;
    color: #8B8B91;
  }

  &__link {
    color: #33976F;
  }

  &__stats {
    position: relative;

    &-percent {
      position: absolute;
      top: 100%;
      left: 0;
      font-size: 11px;
      line-height: 14px;

      &--bad {
        color: #CC2A2A;
      }

      &--good {
        color: #33976F;
      }
    }
  }
}

.seller-items-table-item {
  display: flex;
  align-items: flex-start;

  ::v-deep(.ui-icon) {
    svg {
      width: 16px;
      height: 16px;
    }
  }

  &__image {
    width: 60px;
    height: 65px;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__info {
    display: grid;
    grid-gap: 6px;
    max-width: 200px;
    margin-left: 16px;
  }

  &__name {
    display: flex;
    align-items: flex-end;
    font-size: 14px;
    line-height: 20px;

    &-box {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    ::v-deep(.ui-icon) {
      display: inline-flex;
    }
  }

  &__article {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(4, auto);
    justify-content: flex-start;
    align-self: start;
    font-size: 13px;
    line-height: 16px;

    span {
      font-weight: 500;
    }
  }

  &__rating {
    display: grid;
    grid-gap: 2px;
    grid-template-columns: repeat(3, auto);
    justify-content: flex-start;
    align-items: center;
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;

    ::v-deep(.ui-icon) {
      svg {
        width: 20px;
        height: 20px;
      }

      path {
        fill: #F2CF3A;
      }
    }
  }

  &__reviews {
    margin-left: 2px;
    font-weight: 400;
    font-size: 12px;
    line-height: 14px;
    color: #8B8B91;
  }
}
</style>
