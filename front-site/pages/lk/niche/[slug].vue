<template>
  <div class="niche-lk">
    <div class="container-lk">
      <div class="niche-lk__box">
        <LkGoBack
          link="/lk"
          text="Вернуться к нишам"
          class="niche-lk__back"
        />

        <h1 class="niche-lk__title">
          {{ slug }}
        </h1>

        <div class="niche-lk__tabs">
          <a
            v-for="item in tabs"
            :key="item.slug"
            :href="`#${item.slug}`"
            :class="['niche-lk__tab niche-lk-tab', { 'niche-lk-tab--active' : item.slug === tabActive }]"
            @click.prevent="navigateTo({ query: { product_id: productId }, hash: `#${item.slug}` })"
          >
            {{ item.label }}
            <!-- <span
              v-if="item.count"
              class="niche-lk-tab__count"
            >
              {{ item.count }}
            </span> -->
          </a>
        </div>

        <hr class="niche-lk__hr">

        <div class="niche-lk__content">
          <transition
            name="fade"
            mode="out-in"
          >
            <LazyLkNicheResume
              v-if="tabActive === 'common'"
            />
            <LazyLkNicheItems
              v-else-if="tabActive === 'items'"
            />
          </transition>
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

const { slug } = route.params
const { product_id: productId } = route.query

const tabActive = ref(null)
const tabs = ref([
  { label: 'Сводка', slug: 'common' },
  { label: 'Товары', slug: 'items', count: '1200' },
  // { label: 'Продавцы', count: '620', active: false },
])

watch(() => route.hash, (hash) => {
  setTab(hash)
})

const setTab = (data) => {
  const hash = (data || route.hash).replace('#', '')
  tabActive.value = hash || 'common'
}

onMounted(() => {
  setTab()
})
</script>

<style lang="scss" scoped>
.niche-lk {
  &__box {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 24px 0 100px;
  }

  &__back {
    margin-bottom: 20px;
  }

  &__title {
    margin-bottom: 26px;
    font-weight: 600;
    font-size: 32px;
    line-height: 40px;
    text-transform: capitalize;
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
}

.niche-lk-tab {
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
