<template>
  <div class="search-lk">
    <div class="search-lk__box">
      <div class="search-lk__aside">
        <div class="search-lk-card">
          <p class="search-lk-card__title">
            Что ищем?
          </p>
          <div class="search-lk-card__list">
            <button
              v-for="(item, i) in types"
              :key="i"
              :class="['search-lk-card__btn', { 'search-lk-card__btn--active' : item.value === type}]"
              @click.prevent="changeType(item.value)"
            >
              {{ item.label }}
            </button>
          </div>
        </div>

        <!-- <div class="search-lk-card">
          <p class="search-lk-card__title">
            Как ищем?
          </p>
          <div class="search-lk-card__list">
            <button
              v-for="(item, i) in listHow"
              :key="i"
              :class="['search-lk-card__btn', { 'search-lk-card__btn--active' : item.value === how}]"
              @click.prevent="how = item.value"
            >
              {{ item.label }}
            </button>
          </div>
        </div> -->
      </div>

      <div class="search-lk__content">
        <div class="search-lk__block">
          <div class="search-lk__form">
            <span class="search-lk__loop">
              <UIBaseIcon name="lk/icon-loop" />
            </span>

            <UIBaseInput
              v-model="search"
              placeholder="Поиск по товару, бренду, продавцу и нише"
              class="search-lk__input"
            />

            <a
              v-if="search"
              href="#"
              class="search-lk__clear"
              @click.prevent="clear()"
            >
              <UIBaseIcon name="lk/icon-close" />
            </a>
          </div>

          <p
            v-if="!isLoadHints && search && hints.length === 0 && results.length === 0"
            class="search-lk__empty"
          >
            По запросу: {{ search }} ничего не найдено.<br>
            Введите запрос заново или воспользуйтесь подсказками
          </p>

          <div class="search-lk__results search-lk-results">
            <div class="search-lk-results__list">
              <div
                v-if="isLoadHints"
                class="search-lk__loader"
              >
                <UILoader />
              </div>
              <template v-else-if="hints.length">
                <div
                  v-for="(item, i) in hints"
                  :key="i"
                  class="search-lk-results__item search-lk-results-item"
                  @click="searchResults(item)"
                >
                  <UIBaseIcon name="lk/icon-loop" />
                  {{ item }}
                </div>
              </template>
            </div>

            <div class="search-lk-results__list">
              <div
                v-if="isLoadResults"
                class="search-lk__loader"
              >
                <UILoader />
              </div>
              <template v-else-if="results.length">
                <NuxtLink
                  v-for="(item, i) in results"
                  :key="i"
                  :to="`/lk/item/${item.product__articul}`"
                  class="search-lk-results__category search-lk-results-category"
                >
                  <div class="search-lk-results-category__name">
                    {{ item.product__name }}
                    <!-- <span class="search-lk-results-category__category">
                      Красота / ногти
                    </span> -->
                  </div>
                  <div class="search-lk-results-category__image">
                    <img
                      v-lazy-load
                      :data-src="getProductUrl(item.product__articul)"
                      alt=""
                    >
                  </div>
                </NuxtLink>
              </template>
            </div>
          </div>

          <!-- <div
            v-if="!search"
            class="search-lk__helper search-lk-helper"
          >
            <p class="search-lk-helper__title">
              Часто ищут:
            </p>
            <div class="search-lk-helper__list">
              <div class="search-lk-helper__item">
                Масло для волос
              </div>
              <div class="search-lk-helper__item">
                Рубашка женская
              </div>
              <div class="search-lk-helper__item">
                Кроссовки для детей
              </div>
              <div class="search-lk-helper__item">
                Протеиновое печенье
              </div>
            </div>
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import debounce from 'lodash/debounce'
import GenerateImgUrl from '@/utils/generateImgUrl.js'

definePageMeta({
  layout: 'lk',
})

const types = [
  { label: 'Товары', value: 'products' },
  { label: 'Категории', value: 'categories' },
  { label: 'Бренды', value: 'brands' },
  { label: 'Продавцы', value: 'suppliers' },
  { label: 'Ключевые слова', value: 'keys' },
]
const type = ref('products')

// const listHow = [
//   { label: 'По названию товара', value: 'name' },
//   { label: 'По артикулу товара', value: 'article' },
//   { label: 'По типу товара', value: 'type' },
// ]

// const how = ref('name')

const search = ref('')

const isLoadHints = ref(false)
const isLoadResults = ref(false)
const hints = ref([])
const results = ref([])

const clear = () => {
  search.value = ''
  hints.value = []
  results.value = []
}

watch(() => search.value, (value) => {
  results.value = []

  if (value && !isLoadResults.value) {
    isLoadHints.value = true
    debounced(search.value)
  }
})

const getProductUrl = (id) => {
  return new GenerateImgUrl(id).url()
}

const searchResults = (query) => {
  search.value = query
  results.value = []

  getResults(query)
}

const changeType = (value) => {
  type.value = value

  if (search.value) {
    isLoadHints.value = true
    hints.value = []
    results.value = []

    getHints()
  }
}

const getHints = async () => {
  const { data } = await useFetch('/api/search', {
    watch: false,
    params: {
      query: search.value,
      view: type.value,
    },
  })
  isLoadHints.value = false

  hints.value = data?.value?.variants || []
}

const getResults = async (query) => {
  isLoadResults.value = true

  const { data } = await useFetch('/api/queries/search', {
    params: {
      watch: false,
      query,
      view: 'products',
    },
  })

  const array = data?.value?.items || []

  results.value.push(...array)

  isLoadResults.value = false
}

const debounced = debounce(getHints, 500)
</script>

<style lang="scss" scoped>
.search-lk {
  &__box {
    display: grid;
    grid-template-columns: 320px 1fr;
    align-items: flex-start;
    justify-content: flex-start;
  }

  &__aside {
    display: grid;
    grid-gap: 28px;
    padding: 60px 28px;
  }

  &__content {
    height: 100%;
    padding: 60px 80px;
    background: var(--white);
  }

  &__block {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 680px;
  }

  &__form {
    position: relative;
  }

  &__loop {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 24px;
    display: flex;
    align-items: center;
    z-index: 1;

    ::v-deep(.ui-icon) {
      svg {
        width: 20px;
        height: 20px;

        & > * {
          fill: var(--grayLight);
        }
      }
    }
  }

  &__input {
    ::v-deep(.input__area) {
      height: 60px;
      padding: 15px 56px;
      font-size: 17px;
      line-height: 20px;
      border-radius: 8px;
    }
  }

  &__clear {
    position: absolute;
    top: 0;
    right: 0;
    padding: 20px;
    z-index: 100;
  }

  &__empty {
    margin-top: 40px;
    line-height: 20px;
  }

  &__helper {
    margin-top: 60px;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 50px 0;
  }
}

.search-lk-card {
  display: flex;
  flex-direction: column;
  padding: 24px 24px 32px;
  background: var(--white);
  border-radius: 8px;

  &__title {
    margin-bottom: 16px;
    font-size: 15px;
    line-height: 18px;
    color: #8B8B91;
  }

  &__list {
    display: flex;
    flex-direction: column;
    grid-gap: 4px;
    align-items: flex-start;
  }

  &__btn {
    padding: 12px 24px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    color: var(--blackMain);
    background: var(--white);
    border: 1px solid #E9E9EA;
    border-radius: 60px;

    &--active {
      color: var(--white);
      background: var(--blackMain);
      border-color: var(--blackMain);
    }
  }
}

.search-lk-helper {
  display: grid;
  grid-gap: 20px;

  &__title {
    font-size: 15px;
    line-height: 18px;
    color: #8B8B91;
  }

  &__list {
    display: grid;
    grid-gap: 20px;
    line-height: 20px;
  }
}

.search-lk-results {
  display: flex;
  flex-direction: column;

  &__list {
    display: flex;
    flex-direction: column;
    padding: 10px 0;
    font-size: 15px;
    line-height: 18px;
    border-bottom: 1px solid #E9E9EA;

    &:last-child {
      border-bottom: 0;
    }
  }

  &__item {
    padding: 10px 0;
  }

  &__category {
    padding: 6px 0;
  }
}

.search-lk-results-item {
  display: grid;
  grid-template-columns: repeat(2, auto);
  grid-gap: 12px;
  align-items: center;
  justify-content: flex-start;
  cursor: pointer;
}

.search-lk-results-category {
  display: flex;
  align-items: center;
  justify-content: space-between;

  &__name {
    display: flex;
    flex-direction: column;
    font-weight: 700;
  }

  &__category {
    margin-top: 4px;
    font-weight: 400;
    font-size: 13px;
    line-height: 16px;
    color: #8B8B91;
  }

  &__image {
    width: 48px;
    height: 48px;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
}
</style>
