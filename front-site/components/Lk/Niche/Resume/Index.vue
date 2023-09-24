<template>
  <div class="niche-resume">
    <template v-if="!isLoading && item">
      <div class="niche-resume__info">
        <LkTableTypes />

        <LkTableDate />
      </div>

      <LkNicheResumePerspective
        :item="item"
        class="niche-resume__perspective"
      />

      <LkNicheResumeTopItems
        class="niche-resume__top-items"
      />

      <LkNicheResumeStats
        :item="item"
        class="niche-resume__stats"
      />
    </template>
    <div
      v-else
      class="niche-resume__loader"
    >
      <UILoader />
    </div>

    <LkNicheResumeGraphic />
  </div>
</template>

<script setup>
const props = defineProps({
  slug: {
    type: String,
    default: '',
  },
})

const isLoading = ref(true)
const item = ref(null)

const getData = async () => {
  isLoading.value = true
  const { data } = await useFetch(`/api/queries/search?query=${props.slug}&view=summary`)

  isLoading.value = false

  item.value = data?.value
}

getData()
</script>

<style lang="scss" scoped>
.niche-resume {
  &__info {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
    margin-bottom: 32px;
  }

  &__perspective, &__top-items, &__stats {
    margin-bottom: 60px;
  }

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 100px 0;
  }
}
</style>
