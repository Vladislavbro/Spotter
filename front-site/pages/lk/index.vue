<template>
  <div class="top">
    <div class="container-lk">
      <div class="top__box">
        <h1 class="top__title">
          Топ ниши
        </h1>

        <div
          v-if="isLoadingPage"
          class="top__loader"
        >
          <UILoader />
        </div>

        <template v-else>
          <div class="top__header">
            <div class="top__header-side">
              <LkTableTypes
                :value="fb"
                @change="changeType"
              />

              <LkTableDate
                @change="changeDate"
              />
            </div>

            <LkTableSort
              is-white
              :array="headColumns"
              :sort-slug="sortSlug"
              :sort-direction="sortDirection"
              @change="changeSort"
            />
          </div>

          <LkTableFilter
            class="top__filter"
            @reset="resetFilters()"
            @submit="setFilters()"
          >
            <UILkFilter
              v-model:from="initialFilters.scoring.from"
              v-model:to="initialFilters.scoring.to"
              label="Оценка"
              :max-value="initialFilters.scoring.maxValue"
            />
            <UILkFilter
              v-model:from="initialFilters.profit.from"
              v-model:to="initialFilters.profit.to"
              label="Объём рынка, ₽"
              :max-value="initialFilters.profit.maxValue"
            />
            <!-- <UILkFilter
              label="Ценовой сегмент, ₽"
              :max-value="999999"
            /> -->
            <UILkFilter
              v-model:from="initialFilters.price_avg.from"
              v-model:to="initialFilters.price_avg.to"
              label="Средний чек, ₽"
              :max-value="initialFilters.price_avg.maxValue"
            />
            <!-- <UILkFilter
              v-model:from="initialFilters.products_solded.from"
              v-model:to="initialFilters.products_solded.to"
              label="Товары с продажами"
              :max-value="initialFilters.products_solded.maxValue"
            /> -->
          </LkTableFilter>

          <div
            v-if="!isLoading"
            class="top__list"
          >
            <LkTopCard
              v-for="item in items"
              :key="item.id"
              :item="item"
            />
          </div>
          <div
            v-else
            class="top__loader"
          >
            <UILoader />
          </div>

          <UILkButton
            v-if="isShowBtn"
            text="Показать ещё"
            full-width
            class="top__show-more"
            @click.prevent="page += 1, getData(false)"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'lk',
})

const headColumns = ref([
  // { label: 'Название, характеристики', sort: false, show: true },
  { label: 'Товары, шт.', slug: 'products_count', sort: true, show: true },
  { label: 'Товары с продажами', slug: 'products_solded_30_fbo', sort: true, show: true },
  { label: 'Средний чек', slug: 'price_avg', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Оборот 1-го', slug: 'product_1_profit', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Оборот 10-го', slug: 'product_10_profit', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Объём рынка', slug: 'profit', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
])

const items = ref([])
const page = ref(1)

const fb = ref('fbo')
const day = ref(null)
const date = ref(null)
const sortSlug = ref('products_count')
const sortDirection = ref('asc')

const initialFilters = reactive({
  scoring: {
    from: 0,
    to: 15,
    minValue: 0,
    maxValue: 15,
  },
  price_avg: {
    from: 0,
    to: 999999,
    minValue: 0,
    maxValue: 999999,
  },
  profit: {
    from: 0,
    to: 9999999999,
    minValue: 0,
    maxValue: 9999999999,
  },
  products_solded: {
    from: 0,
    to: 999999,
    minValue: 0,
    maxValue: 999999,
  },
})
const filters = ref({})

const isShowBtn = ref(true)
const isLoadingPage = ref(true)
const isLoading = ref(false)

const changeType = (value) => {
  items.value = []
  page.value = 1
  fb.value = value

  updateSort()

  getData()
}

const changeDate = (data) => {
  items.value = []
  page.value = 1
  day.value = data.day
  date.value = data.date

  updateSort()

  getData()
}

const updateSort = () => {
  const newSortSlug = `products_solded_${day.value}_${fb.value}`

  if (sortSlug.value.startsWith('products_solded')) {
    sortSlug.value = newSortSlug
  }

  headColumns.value.find((item) => {
    if (item.slug.startsWith('products_solded')) {
      item.slug = newSortSlug
      return true
    }
    return false
  })
}

const changeSort = (obj) => {
  items.value = []
  page.value = 1
  sortSlug.value = obj.slug
  sortDirection.value = obj.direction

  getData()
}

const resetFilters = () => {
  for (const key in initialFilters) {
    initialFilters[key].from = initialFilters[key].minValue
    initialFilters[key].to = initialFilters[key].maxValue
  }

  filters.value = {}
}

const setFilters = () => {
  items.value = []
  page.value = 1
  isShowBtn.value = true

  for (const key in initialFilters) {
    if (initialFilters[key].from !== initialFilters[key].minValue || initialFilters[key].to !== initialFilters[key].maxValue) {
      let query = ''
      query += initialFilters[key].from !== initialFilters[key].minValue ? `${initialFilters[key].from};` : ';'
      query += initialFilters[key].to !== initialFilters[key].maxValue ? `${initialFilters[key].to}` : ''

      filters.value[key] = query
    }
  }

  getData()
}

const getData = async (isPreloading = true) => {
  if (isPreloading) {
    isLoading.value = true
  }

  let params = {
    output: 'json',
    page: page.value,
    sort: sortSlug.value,
    direction: sortDirection.value,
    fb: fb.value,
  }

  if (day.value) {
    params.period = day.value
  }

  if (date.value) {
    params.dateTo = date.value
  }

  if (Object.keys(filters.value).length) {
    params = {
      ...params,
      ...filters.value,
    }
  }

  const { data } = await useFetch('/api/queries/top', {
    params,
    watch: false,
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

await getData()
</script>

<style lang="scss" scoped>
.top {
  &__box {
    display: flex;
    flex-direction: column;
    padding: 32px 0 100px;
  }

  &__title {
    margin-bottom: 20px;
    font-family: 'Hauora';
    font-weight: 700;
    font-size: 32px;
    line-height: 40px;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;

    margin: 50px auto;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 32px;
  }

  &__header-side {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
  }

  &__filter {
    margin-bottom: 32px;
  }

  &__list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
    align-items: flex-start;
    justify-content: flex-start;
  }

  // &__card {
  //   display: flex;
  //   flex-direction: column;
  //   margin-bottom: 40px;
  //   padding: 24px 20px 20px;
  //   background: var(--white);
  //   border-radius: 12px;
  // }

  // &__card-header {
  //   display: flex;
  //   align-items: center;
  //   justify-content: space-between;
  //   margin-bottom: 24px;
  // }

  // &__card-side {
  //   display: grid;
  //   grid-gap: 8px;
  //   grid-template-columns: repeat(2, auto);
  // }

  &__show-more {
    height: 48px;
    margin-top: 40px;

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

// .top-table {
//   tr {
//     &:hover {
//       .top-table {
//         &__description {
//           white-space: normal;
//         }
//       }
//     }
//   }

//   &__name {
//     display: grid;
//     grid-gap: 2px;
//   }

//   &__link {
//     color: #33976F;
//   }

//   &__description {
//     font-size: 13px;
//     line-height: 16px;
//     white-space: nowrap;
//     overflow: hidden;
//     text-overflow: ellipsis;
//     max-width: 300px;
//   }

//   &__stats {
//     position: relative;

//     &-percent {
//       position: absolute;
//       top: 100%;
//       left: 0;
//       font-size: 11px;
//       line-height: 14px;

//       &--bad {
//         color: #CC2A2A;
//       }

//       &--good {
//         color: #33976F;
//       }
//     }
//   }
// }
</style>
