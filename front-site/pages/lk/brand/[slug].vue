<template>
  <div class="brand-lk">
    <div class="container-lk">
      <div class="brand-lk__box brand-lk__box--pad">
        <LkGoBack
          to="/lk"
          text="Вернуться к товарам"
          class="brand-lk__back"
        />

        <div class="brand-lk__box">
          <div class="brand-lk__card brand-lk-card">
            <p class="brand-lk-card__label">
              <UIBaseIcon name="lk/icon-wb" />
              Бренды
            </p>
            <a
              :href="wbLink"
              target="_blank"
              class="brand-lk-card__link"
            >
              {{ brandName }}
              <UIBaseIcon name="lk/icon-share" />
            </a>
          </div>

          <div class="brand-lk__tabs">
            <button
              v-for="(item, i) in tabs"
              :key="i"
              :class="['brand-lk-card__tab brand-lk-tab', { 'brand-lk-tab--active' : item.active }]"
              @click.prevent="toggleTab(i)"
            >
              {{ item.label }}
              <!-- <span
                v-if="item.count"
                class="brand-lk-tab__count"
              >
                {{ item.count }}
              </span> -->
            </button>
          </div>

          <hr class="brand-lk__hr">

          <div class="brand-lk__content">
            <transition
              name="fade"
              mode="out-in"
            >
              <LazyLkBrandResume
                v-if="tabs[0].active"
              />
              <LazyLkBrandItems
                v-else-if="tabs[1].active"
              />
              <LazyLkBrandSellers
                v-else-if="tabs[2].active"
              />
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'lk',
})

const route = useRoute()

const { name: brandName } = route.query
const { slug } = route.params

const tabs = ref([
  { label: 'Сводка', active: true },
  { label: 'Товары', active: false },
  { label: 'Продавцы', active: false },
])

const toggleTab = (i) => {
  tabs.value.forEach((item) => {
    item.active = false
  })
  tabs.value[i].active = true
}

const wbLink = computed(() => {
  let name = '#'
  if (brandName && slug) {
    name = `https://www.wildberries.ru/brands/${brandName.toLowerCase()}-${slug}`
  }
  return name
})
</script>

<style lang="scss" scoped>
.brand-lk {
  &__box {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    &--pad {
      padding: 24px 0 100px;
    }
  }

  &__back {
    margin-bottom: 24px;
  }

  &__card {
    margin-bottom: 32px;
  }

  &__tabs {
    display: flex;
    align-items: center;
    padding: 6px;
    background: #E9EAEC;
    border-radius: 120px;
  }

  &__hr {
    width: calc(100% + 54px + 60px);
    margin: 24px -54px 24px -60px;
    border-color: #E2E2E7;
  }

  &__content {
    width: 100%;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 100px auto;
  }
}

.brand-lk-card {
  width: 100%;
  display: grid;
  grid-gap: 8px;
  justify-content: flex-start;
  padding: 24px 40px 32px;
  background: var(--white);
  border-radius: 16px;

  &__label {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    justify-content: flex-start;
    align-items: center;
    font-weight: 500;
    font-size: 15px;
    line-height: 18px;
    color: #9D9DA5;
  }

  &__link {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: flex-start;
    font-weight: 600;
    font-size: 24px;
    line-height: 32px;
    text-transform: capitalize;
  }
}

.brand-lk-tab {
  display: flex;
  align-items: center;
  height: 44px;
  padding: 10px 20px;
  font-weight: 500;
  font-size: 16px;
  line-height: 24px;

  &:hover, &--active {
    color: var(--white);
    background: #8557E5;
    box-shadow: 0px 2px 6px rgba(42, 46, 59, 0.24);
    border-radius: 120px;
  }

  &__count {
    align-self: flex-start;
    margin-left: 2px;
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;
    color: #9D9DA5;
  }
}
</style>
