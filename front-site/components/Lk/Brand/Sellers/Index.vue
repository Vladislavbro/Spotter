<template>
  <div class="brand-sellers">
    <template v-if="!isLoadingPage">
      <div class="brand-sellers__info">
        <LkTableDate
          @change="changeDate"
        />
      </div>

      <div class="brand-sellers__card">
        <div class="brand-sellers__card-header">
          <div class="brand-sellers__card-side">
            <LkTableSettings
              :array="headColumns"
            />
          </div>
        </div>

        <LkTable
          v-if="!isLoading"
          :head-columns="headColumns"
          class="brand-sellers__table brand-sellers-table"
        >
          <tbody>
            <tr
              v-for="(item, i) in items"
              :key="i"
            >
              <td v-if="headColumns[0].show">
                <NuxtLink
                  :to="`/lk/seller/${item.wb_id}?name=${item.name}`"
                  class="brand-sellers-table__name"
                >
                  {{ item.name }}
                </NuxtLink>
              </td>
              <td v-if="headColumns[1].show">
                {{ item.inn }}
              </td>
              <td v-if="headColumns[2].show">
                {{ item.ogrn }}
              </td>
              <td v-if="headColumns[3].show">
                {{ item.trademark }}
              </td>
            </tr>
          </tbody>
        </LkTable>

        <div
          v-else
          class="brand-sellers__loader"
        >
          <UILoader />
        </div>
      </div>
    </template>
    <div
      v-else
      class="brand-sellers__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
const route = useRoute()

const { slug } = route.params

const headColumns = ref([
  { label: 'Продавец', slug: 'name', show: true },
  { label: 'ИНН', slug: 'inn', show: true },
  { label: 'ОГРН', slug: 'ogrn', show: true },
  { label: 'Торговая марка', slug: 'trademark', show: true },
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

  const { data } = await useFetch(`/api/brands/${slug}`, {
    watch: false,
    query: {
      view: 'suppliers',
      period: day.value,
    },
  })

  items.value = data?.value?.suppliers || []

  isLoadingPage.value = false
  isLoading.value = false
}

getData()
</script>

<style lang="scss" scoped>
.brand-sellers {
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

.brand-sellers-table {
  &__name {
    display: flex;
    align-items: center;
    color: #33976F;
  }
}
</style>
