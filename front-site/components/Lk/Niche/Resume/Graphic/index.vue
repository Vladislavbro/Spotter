<template>
  <div class="resume-graphic">
    <div class="resume-graphic__header">
      <p class="resume-graphic__title">
        Изменения показателей
      </p>

      <LkTableDate
        calendar-only
      />
    </div>

    <div class="resume-graphic__checkboxes">
      <label
        v-for="(item, i) in checkboxes"
        :key="i"
        :class="['resume-graphic__checkbox resume-graphic-checkbox', { 'resume-graphic-checkbox--checked' : item.value }]"
      >
        <div class="resume-graphic-checkbox__content">
          <p class="resume-graphic-checkbox__label">
            {{ item.label }}
          </p>
          <p class="resume-graphic-checkbox__count">
            {{ item.count }}
          </p>
        </div>
        <input
          v-model="item.value"
          type="checkbox"
        >
        <span
          class="resume-graphic-checkbox__box"
        />
      </label>
    </div>

    <div class="resume-graphic__charts">
      <LkChart
        :data="data"
        :options="options"
      />
    </div>
  </div>
</template>

<script setup>
const checkboxes = ref([
  { label: 'Оборот', value: true, count: '56 425 866 ₽' },
  { label: 'Средний чек', value: true, count: '940 ₽' },
  { label: 'Продажи', value: true, count: '2 174 шт' },
  { label: 'Кол-во товаров', value: true, count: '31 шт' },
  { label: 'Продавцы', value: true, count: '12 шт' },
  { label: 'Бренды', value: true, count: '9 шт' },
])

const data = {
  labels: [],
  datasets: [
    {
      label: 'Оборот',
      valueSuffix: '₽',
      borderColor: '#FF8F6D',
      pointBorderColor: '#FF8F6D',
      data: [],
    },
    {
      label: 'Средний чек',
      valueSuffix: '₽',
      borderColor: '#F488D7',
      pointBorderColor: '#F488D7',
      data: [],
    },
    {
      label: 'Продажи',
      valueSuffix: 'шт.',
      borderColor: '#AE80EA',
      pointBorderColor: '#AE80EA',
      data: [],
    },
    {
      label: 'Кол-во товаров',
      valueSuffix: 'шт.',
      borderColor: '#5480F2',
      pointBorderColor: '#5480F2',
      data: [],
    },
    {
      label: 'Продавцы',
      valueSuffix: 'шт.',
      borderColor: '#6DC68B',
      pointBorderColor: '#6DC68B',
      data: [],
    },
    {
      label: 'Бренды',
      valueSuffix: 'шт.',
      borderColor: '#F4D037',
      pointBorderColor: '#F4D037',
      data: [],
    },
  ],
}

const options = {}

const setDefault = () => {
  const labels = []
  for (let i = 10; i <= 28; i++) {
    labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
  }
  data.labels = labels

  const values1 = []
  const values2 = []
  const values3 = []
  const values4 = []
  const values5 = []
  const values6 = []

  for (let i = 0; i <= 18; i++) {
    values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
    values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
    values3.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
    values4.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
    values5.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
    values6.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
  }
  data.datasets[0].data = values1
  data.datasets[1].data = values2
  data.datasets[2].data = values3
  data.datasets[3].data = values4
  data.datasets[4].data = values5
  data.datasets[5].data = values6
}

setDefault()
</script>

<style lang="scss" scoped>
.resume-graphic {
  display: flex;
  flex-direction: column;
  padding: 24px 40px 40px;
  background: var(--white);
  border-radius: 16px;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
  }

  &__title {
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__checkboxes {
    display: grid;
    grid-gap: 12px;
    grid-template-columns: repeat(6, 1fr);
    align-items: flex-start;
    justify-content: flex-start;
  }

  &__charts {
    width: 100%;
    height: 420px;
    margin-top: 40px;
  }
}

.resume-graphic-checkbox {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 16px 12px;
  background: var(--white);
  border: 1px solid #E2E2E7;
  border-radius: 8px;
  cursor: pointer;

  &--checked {
    background: #B7CFFF;
    border-color: #B7CFFF;

    .resume-graphic-checkbox {
      &__box {
        background: #5081FE url(~/assets/icons/lk/icon-check.svg)no-repeat 50%;
        border-color: #5081FE;
      }
    }
  }

  input {
    display: none;
  }

  &__content {
    display: grid;
    grid-gap: 8px;
    font-size: 15px;
    line-height: 18px;
  }

  &__count {
    font-weight: 600;
  }

  &__box {
    display: block;
    width: 24px;
    height: 24px;
    background: var(--white);
    border: 1px solid #D9D9E0;
    border-radius: 4px;
  }
}
</style>
