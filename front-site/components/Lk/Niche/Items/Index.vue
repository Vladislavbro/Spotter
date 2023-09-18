<template>
  <div class="niche-items">
    <template v-if="!isLoadingPage">
      <div class="niche-items__info">
        <LkTableTypes
          :value="fb"
          @change="changeType"
        />

        <LkTableDate />
      </div>

      <!-- <LkTableFilter class="niche-items__filter">
        <UILkFilter
          label="Рейтинг"
        />
        <UILkFilter
          label="Оборот"
        />
        <UILkFilter
          label="Продажи, шт"
        />
      </LkTableFilter> -->

      <div class="niche-items__card">
        <div class="niche-items__card-header">
          <div class="niche-items__card-side">
            <LkTableSettings
              :array="headColumns"
            />

            <LkTableSort
              :array="headColumns"
              :sort-slug="sortSlug"
              :sort-direction="sortDirection"
              @change="changeSort"
            />
          </div>

          <LkTableImport />
        </div>

        <LkTable
          :head-columns="headColumns"
          class="niche-items__table niche-items-table"
        >
          <tbody>
            <tr
              v-for="(item, i) in items"
              :key="i"
            >
              <td v-if="headColumns[0].show">
                <div class="niche-items-table-item">
                  <!-- <div class="niche-items-table-item__image">
                    <img
                      src="@/assets/images/lk/item-niche-items-test.jpg"
                      alt=""
                    >
                  </div> -->
                  <div class="niche-items-table-item__info">
                    <NuxtLink
                      :to="`/lk/item/${item.product__articul}`"
                      class="niche-items-table-item__name"
                    >
                      <span class="niche-items-table-item__name-box">
                        {{ item.product__name }}
                      </span>
                      <UIBaseIcon name="lk/icon-share" />
                    </NuxtLink>
                    <button
                      class="niche-items-table-item__article"
                      rel="nofollow"
                      @click.prevent="copyText(item.product__articul)"
                    >
                      <UIBaseIcon name="lk/icon-wb" />
                      <span>
                        Артикул:
                      </span>
                      {{ item.product__articul }}
                      <UIBaseIcon name="lk/icon-copy" />
                    </button>
                    <p class="niche-items-table-item__rating">
                      <UIBaseIcon name="lk/icon-star" />
                      {{ item.product__rating }}
                      <span class="niche-items-table-item__reviews">
                        ({{ item.product__feedbacks }} отзывов)
                      </span>
                    </p>
                  </div>
                </div>
              </td>
              <td v-if="headColumns[1].show">
                <div class="niche-items-table__price">
                  <p class="niche-items-table__newprice">
                    {{ item?.price.toLocaleString() || 0 }} ₽
                    <span class="niche-items-table__price-percent">
                      {{ parseInt(100 - item.price / ( item.priceU / 100 )) }}%
                    </span>
                  </p>
                  <span class="niche-items-table__oldprice">
                    {{ item?.priceU.toLocaleString() || 0 }} ₽
                  </span>
                </div>
              </td>
              <!-- <td>
                <NuxtLink
                  to="/lk/seller/1"
                  class="niche-items-table__link"
                >
                  {{ item.seller }}
                </NuxtLink>
              </td>
              <td>
                <NuxtLink
                  to="/lk/seller/1"
                  class="niche-items-table__link"
                >
                  {{ item.brand }}
                </NuxtLink>
              </td> -->
              <td v-if="headColumns[2].show">
                <p class="niche-items-table__stats">
                  {{ item?.profit_30_fbo.toLocaleString() || 0 }} ₽
                  <!-- <span class="niche-items-table__stats-percent niche-items-table__stats-percent--good">
                    {{ item.turnover_percent }}
                  </span> -->
                </p>
              </td>
              <td v-if="headColumns[3].show">
                <p class="niche-items-table__stats">
                  {{ item?.sales_30_fbo.toLocaleString() || 0 }}
                  <!-- <span class="niche-items-table__stats-percent niche-items-table__stats-percent--good">
                    {{ item.sales_percent }}
                  </span> -->
                </p>
              </td>
            </tr>
          </tbody>
        </LkTable>
      </div>

      <UILkButton
        v-if="isShowBtn"
        text="Показать ещё"
        full-width
        class="niche-items__show-more"
        @click.prevent="page += 1, getData()"
      />
    </template>
    <div
      v-else
      class="niche-items__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
import copyTextToClipboard from '@/utils/copyTextToClipboard'

const props = defineProps({
  slug: {
    type: String,
    default: '',
  },
})

const isLoading = ref(false)
const isLoadingPage = ref(true)
const items = ref([])
const page = ref(1)
const fb = ref('fbo')
const sortSlug = ref('price')
const sortDirection = ref('asc')

const changeType = (value) => {
  items.value = []
  page.value = 1
  fb.value = value

  getData()
}

const changeSort = (obj) => {
  items.value = []
  page.value = 1
  sortSlug.value = obj.slug
  sortDirection.value = obj.direction

  getData()
}

const headColumns = ref([
  { label: 'Название товара', show: true },
  { label: 'Цена', slug: 'price', sort: true, show: true },
  // { label: 'Продавец', show: true },
  // { label: 'Бренд', show: true },
  { label: 'Оборот', slug: 'profit', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Продажи, шт.', slug: 'sales', sort: true, show: true },
])

const copyText = async (text) => {
  const msg = await copyTextToClipboard(text)
}

const getData = async () => {
  isLoading.value = true
  const { data } = await useFetch(`/api/queries/search?query=${props.slug}&view=products`, {
    // lazy: true,
    // server: false,
    watch: false,
    params: {
      page: page.value,
      sort: sortSlug.value,
      direction: sortDirection.value,
      fb: fb.value,
    },
  })

  const total = data?.value?.total || 0
  const array = data?.value?.items || []

  items.value.push(...array)

  isLoadingPage.value = false
  isLoading.value = false

  if (items.value.length >= total) {
    isShowBtn.value = false
  }
}

getData()
</script>

<style lang="scss" scoped>
.niche-items {
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

  &__show-more {
    height: 48px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    color: var(--blackMain);
    background: none;
    border-color: #D9D9E0;

    &:hover {
      background: none;
    }
  }
}

.niche-items-table {
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

.niche-items-table-item {
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
