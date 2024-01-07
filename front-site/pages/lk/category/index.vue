<template>
  <div class="category">
    <div class="container-lk">
      <div class="category__box">
        <h1 class="category__title">
          Категории
        </h1>

        <div class="category__header">
          <LkTableTypes
            :value="fb"
            @change="changeType"
          />

          <LkTableDate
            @change="changeDate"
          />
        </div>

        <!-- <LkTableFilter class="category__filter">
          <UILkFilter
            label="Оброот"
          />
          <UILkFilter
            label="Средняя цена"
          />
          <UILkFilter
            label="Процент товаров с продажами"
          />
        </LkTableFilter> -->

        <div class="category__card">
          <div class="category__card-header">
            <div class="category__card-side">
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
            v-if="!isLoading"
            :head-columns="headColumns"
            class="category__table category-table"
          >
            <tbody>
              <template
                v-for="(item, i) in items"
                :key="i"
              >
                <LkTableCategoryRow
                  :item="item"
                />
              </template>
            </tbody>
          </LkTable>
          <div
            v-else
            class="category__loader"
          >
            <UILoader />
          </div>
        </div>

        <UILkButton
          v-if="isShowBtn"
          text="Показать ещё"
          full-width
          class="category__show-more"
          @click.prevent="page += 1, getData(false)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'lk',
})

const headColumns = ref([
  { label: 'Категория', show: true },
  { label: 'Товары, шт', slug: 'products_count', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Продавцов, шт', slug: 'sellers_count', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Брендов, шт', show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Оборот', slug: 'profit', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Средняя цена', slug: 'price_avg', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Продавцы с продажами', slug: 'products_solded', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Бренды с продажами', show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Товары с продажами', slug: 'sellers_solded', sort: true, show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Среднее кол-во продаж на товар', show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  // { label: 'Среднее кол-во продаж на продавца', show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
])
const items = ref([])
const page = ref(1)

const fb = ref('fbo')
const day = ref(null)
const date = ref(null)
const sortSlug = ref('products_count')
const sortDirection = ref('asc')

const isShowBtn = ref(false)
const isLoading = ref(false)

const changeType = (value) => {
  items.value = []
  page.value = 1
  fb.value = value

  getData()
}

const changeDate = (data) => {
  items.value = []
  page.value = 1
  day.value = data.day
  date.value = data.date

  getData()
}

const changeSort = (obj) => {
  items.value = []
  page.value = 1
  sortSlug.value = obj.slug
  sortDirection.value = obj.direction

  getData()
}

const getData = async (isPreloading = true) => {
  if (isPreloading) {
    isLoading.value = true
  }

  const params = {
    output: 'json',
    page: page.value,
    // sort: sortSlug.value,
    direction: sortDirection.value,
    fb: fb.value,
  }

  if (day.value) {
    params.period = day.value
  }

  if (date.value) {
    params.dateTo = date.value
  }

  const { data } = await useFetch('/api/categories', {
    params,
    watch: false,
  })

  isLoading.value = false

  const total = data?.value?.total || 0
  const array = data?.value?.items || []

  items.value.push(...array)

  if (items.value.length >= total) {
    isShowBtn.value = false
  }
}

getData()
</script>

<style lang="scss" scoped>
.category {
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
</style>
