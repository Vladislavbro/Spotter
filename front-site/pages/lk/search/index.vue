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
              v-for="(item, i) in listWhat"
              :key="i"
              :class="['search-lk-card__btn', { 'search-lk-card__btn--active' : item.value === what}]"
              @click.prevent="what = item.value"
            >
              {{ item.label }}
            </button>
          </div>
        </div>

        <div class="search-lk-card">
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
        </div>
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

          <!-- <div
            v-if="isLoading"
            class="search-lk__loader"
          >
            <UILoader />
          </div> -->
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
                >
                  <UIBaseIcon name="lk/icon-loop" />
                  {{ item }}
                </div>
              </template>
              <!-- <div class="search-lk-results__item search-lk-results-item">
                <UIBaseIcon name="lk/icon-loop" />
                Масло для губ
              </div>
              <div class="search-lk-results__item search-lk-results-item">
                <UIBaseIcon name="lk/icon-loop" />
                Масло для кутикулы
              </div>
              <div class="search-lk-results__item search-lk-results-item">
                <UIBaseIcon name="lk/icon-loop" />
                Масло для волос
              </div> -->
            </div>

            <div class="search-lk-results__list">
              <div
                v-if="isLoadResults"
                class="search-lk__loader"
              >
                <UILoader />
              </div>
              <template v-else-if="results.length">
                <div
                  v-for="(item, i) in results"
                  :key="i"
                  class="search-lk-results__category search-lk-results-category"
                >
                  {{ item }}
                  <div class="search-lk-results-category__name">
                    Уход за ногятми
                    <span class="search-lk-results-category__category">
                      Красота / ногти
                    </span>
                  </div>
                  <div class="search-lk-results-category__image">
                    <img src="@/assets/images/lk/search-dropdown-test.jpg" alt="">
                  </div>
                </div>
              </template>
              <!-- <div class="search-lk-results__category search-lk-results-category">
                <div class="search-lk-results-category__name">
                  Уход за ногятми
                  <span class="search-lk-results-category__category">
                    Красота / ногти
                  </span>
                </div>
                <div class="search-lk-results-category__image">
                  <img src="@/assets/images/lk/search-dropdown-test.jpg" alt="">
                </div>
              </div> -->
            </div>
          </div>

          <!-- <p
            v-else-if="!isLoading && search && items.length === 0"
            class="search-lk__empty"
          >
            По запросу: {{ search }} ничего не найдено.<br>
            Введите запрос заново или воспользуйтесь подсказками
          </p> -->

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

definePageMeta({
  layout: 'lk',
})

const listWhat = [
  { label: 'Товары', value: 'items' },
  { label: 'Категории', value: 'categories' },
  { label: 'Бренды', value: 'brands' },
  { label: 'Продавцы', value: 'sellers' },
  { label: 'Ключевые слова', value: 'words' },
]

const listHow = [
  { label: 'По названию товара', value: 'name' },
  { label: 'По артикулу товара', value: 'article' },
  { label: 'По типу товара', value: 'type' },
]

const what = ref('items')
const how = ref('name')

const search = ref('')

// const isLoading = ref(false)
// const items = ref([])

const isLoadHints = ref(false)
const isLoadResults = ref(false)
const hints = ref([])
const results = ref([])

const clear = () => {
  search.value = ''
}

watch(() => search.value, (value) => {
  if (value) {
    isLoadHints.value = true
    debounced(search.value)
  }
})

const getHints = async () => {
  const { data } = await useFetch('/api/search', {
    params: {
      query: search.value,
    },
  })
  isLoadHints.value = false

  hints.value = data?.value?.variants || []
}

const getResults = async () => {

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
    border-top: 1px solid #E9E9EA;

    &:first-child {
      border-top: 0;
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
}
</style>
