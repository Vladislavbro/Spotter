<template>
  <div class="resume-stats">
    <p class="resume-stats__title">
      Основные показатели
    </p>

    <div class="resume-stats__cards">
      <LkNicheResumeStatsCard
        v-for="(card, i) in cards"
        :key="i"
        :item="card"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})

const cards = ref([
  { title: 'Объём рынка', type: 'up', price: '0', diff: '0', percent: '0' },
  { title: 'LP', type: 'up', price: '0', diff: '0', percent: '0' },
  { title: 'Общий потенциал рынка', type: 'up', price: '0', diff: '0', percent: '0' },
  { title: 'Объём рынка у ТОП-10', type: 'up', price: '0', diff: '0', percent: '0' },
  { title: 'SPP', type: 'up', price: '0', diff: '', percent: '0' },
])

const setDefault = () => {
  cards.value[0].price = `${props.item?.profit?.toLocaleString()} ₽`
  cards.value[0].percent = parseInt((props.item?.volume || 0) * 100) / 100

  cards.value[1].price = `${props.item?.profit_lost?.toLocaleString()} ₽`

  cards.value[3].price = `${props.item?.profit_top_sup?.toLocaleString()} ₽`
  cards.value[3].percent = parseInt((props.item?.profit_top_sup_diff || 0) * 100) / 100

  cards.value[4].price = `${parseInt((props.item?.product_solded_diff || 0) * 100) / 100} %`
}

setDefault()
</script>

<style lang="scss" scoped>
.resume-stats {
  display: flex;
  flex-direction: column;
  padding: 40px 40px 48px;
  color: var(--white);
  background: #232328;
  border-radius: 16px;

  &__title {
    margin-bottom: 28px;
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__cards {
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(5, 1fr);
    align-items: flex-start;
  }
}
</style>
