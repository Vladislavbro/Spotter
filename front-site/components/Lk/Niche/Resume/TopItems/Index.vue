<template>
  <div class="top-items">
    <p class="top-items__title">
      ТОП-5 товаров ниши
    </p>

    <div
      v-if="!isLoading"
      class="top-items__cards"
    >
      <LkNicheResumeTopItemsCard
        v-for="(item, i) in items"
        :key="i"
        :item="item"
        :type="fb"
        :day="day"
      />
    </div>
    <div
      v-else
      class="top-items__loader"
    >
      <UILoader />
    </div>

    <UILkButton
      text="Смотреть все товары"
      class="top-items__btn"
      @click="navigateTo({ query: { product_id: productId }, hash: '#items' })"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  fb: {
    type: String,
    default: 'fbo',
  },
  day: {
    type: Number,
    default: 30,
  },
})

const route = useRoute()

const { slug } = route.params
const { product_id: productId } = route.query

const items = ref([])
const isLoading = ref(true)

watch(() => props.fb, () => {
  getItems()
})

watch(() => props.day, () => {
  getItems()
})

const getItems = async () => {
  isLoading.value = true
  items.value = []

  const params = {
    output: 'json',
    fb: props.fb,
  }

  if (productId) {
    params.product_id = productId
  }

  if (props.day) {
    params.period = props.day
  }

  const { data } = await useFetch(`/api/queries/search?query=${slug}&view=products`, {
    watch: false,
    params: {
      ...params,
      sort: `profit_${props.day}_${props.fb}`,
      direction: 'desc',
      per_page: 5,
    },
  })
  isLoading.value = false

  items.value = data?.value?.items || []
}

getItems()
</script>

<style lang="scss" scoped>
.top-items {
  display: flex;
  flex-direction: column;

  &__title {
    margin-bottom: 28px;
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__cards {
    display: grid;
    grid-gap: 16px;
    grid-template-columns: repeat(5, 1fr);
    margin-bottom: 32px;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 32px;
  }

  &__btn {
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
