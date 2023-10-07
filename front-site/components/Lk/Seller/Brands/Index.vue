<template>
  <div class="seller-brands">
    <template v-if="!isLoadingPage">
      <div class="seller-brands__info">
        <LkTableDate
          @change="changeDate"
        />
      </div>

      <div class="seller-brands__card">
        <div class="seller-brands__card-header">
          <div class="seller-brands__card-side">
            <LkTableSettings
              :array="headColumns"
            />
          </div>
        </div>

        <LkTable
          v-if="!isLoading"
          :head-columns="headColumns"
          class="seller-brands__table seller-brands-table"
        >
          <tbody>
            <tr
              v-for="(item, i) in items"
              :key="i"
            >
              <td v-if="headColumns[0].show">
                <NuxtLink
                  :to="`/lk/brand/${item.brand_id}?name=${item?.brand?.toLowerCase() || ''}`"
                  class="seller-brands-table__name"
                >
                  {{ item.brand }}
                </NuxtLink>
              </td>
            </tr>
          </tbody>
        </LkTable>

        <div
          v-else
          class="seller-brands__loader"
        >
          <UILoader />
        </div>
      </div>
    </template>
    <div
      v-else
      class="seller-brands__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
const route = useRoute()

const { slug } = route.params

const headColumns = ref([
  { label: 'Бренд', slug: 'brand', show: true },
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

const getData = async () => {
  isLoading.value = true

  const { data } = await useFetch(`/api/suppliers/${slug}`, {
    watch: false,
    query: {
      view: 'brands',
      period: day.value,
    },
  })

  items.value = data?.value?.brands || []

  isLoadingPage.value = false
  isLoading.value = false
}

getData()
</script>

<style lang="scss" scoped>
.seller-brands {
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

.seller-brands-table {
  &__name {
    display: flex;
    align-items: center;
    color: #33976F;
  }
}
</style>
