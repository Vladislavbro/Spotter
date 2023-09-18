<template>
  <div class="seller-resume">
    <div class="seller-resume__info">
      <!-- <LkTableTypes /> -->

      <LkTableDate />
    </div>

    <div class="seller-resume__graphics">
      <div class="seller-resume__graphic seller-resume-graphic">
        <p class="seller-resume-graphic__title">
          Оборот и средний чек
        </p>
        <div class="seller-resume-graphic__badges">
          <span class="badge badge--blue">
            Оборот по заказам:
            <span class="badge__value">
              10 425 866 ₽
            </span>
          </span>
          <span class="badge badge--purple">
            Оборот по продажам:
            <span class="badge__value">
              10 425 866 ₽
            </span>
          </span>
          <span class="badge">
            Оборот по счетчику WB:
            <span class="badge__value">
              8 425 866 ₽
            </span>
          </span>
          <span class="badge badge--orange">
            Средний чек:
            <span class="badge__value">
              866 ₽
            </span>
          </span>
        </div>

        <div class="seller-resume-graphic__chart">
          <LkChart
            :data="data1"
            :options="options"
          />
        </div>
      </div>

      <!-- <div class="seller-resume__graphic seller-resume-graphic">
        <p class="seller-resume-graphic__title">
          Остатки, возвраты и поставки
        </p>
        <div class="seller-resume-graphic__badges">
          <span class="badge badge--green">
            Остатки:
            <span class="badge__value">
              75,9%
            </span>
          </span>
          <span class="badge badge--yellow">
            Возвраты и поставки:
            <span class="badge__value">
              24%
            </span>
          </span>
        </div>

        <div class="seller-resume-graphic__chart">
          <LkChart
            :data="data2"
            :options="options"
          />
        </div>
      </div> -->
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  graphs: {
    type: Array,
    default: () => ([]),
  },
})

// let width, height
// function getGradient (ctx, chartArea, colors) {
//   const chartWidth = chartArea.right - chartArea.left
//   const chartHeight = chartArea.bottom - chartArea.top
//   let gradient
//   if (!gradient || width !== chartWidth || height !== chartHeight) {
//     width = chartWidth
//     height = chartHeight
//     gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top)
//     gradient.addColorStop(1, colors[0])
//     gradient.addColorStop(0, colors[1])
//   }

//   return gradient
// }

const data1 = {
  labels: [],
  datasets: [
    {
      label: 'Оборот по заказам',
      valueSuffix: '₽',
      borderColor: '#5480F2',
      pointBorderColor: '#5480F2',
      data: [],
    },
    {
      label: 'Оборот по продажам',
      valueSuffix: '₽',
      borderColor: '#AE80EA',
      pointBorderColor: '#AE80EA',
      data: [],
    },
    {
      label: 'Средний чек',
      valueSuffix: '₽',
      borderColor: '#FF8F6D',
      pointBorderColor: '#FF8F6D',
      data: [],
    },
  ],
}

// const data2 = {
//   labels: [],
//   datasets: [
//     {
//       label: 'Остатки',
//       valueSuffix: 'шт.',
//       borderColor: '#22A873',
//       pointBorderColor: '#22A873',
//       data: [],
//     },
//     {
//       label: 'Возвраты и поставки',
//       valueSuffix: 'шт.',
//       borderColor: '#98D920',
//       pointBorderColor: '#98D920',
//       data: [],
//     },
//   ],
// }

const options = {}

const setDefault1 = () => {
  const labels = []
  for (let i = 10; i <= 28; i++) {
    labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
  }
  data1.labels = labels

  const values1 = []
  const values2 = []
  const values3 = []

  for (let i = 0; i <= 18; i++) {
    values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
    values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
    values3.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
  }
  data1.datasets[0].data = values1
  data1.datasets[1].data = values2
  data1.datasets[2].data = values3
}

// const setDefault2 = () => {
//   const labels = []
//   for (let i = 10; i <= 28; i++) {
//     labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
//   }
//   data2.labels = labels

//   const values1 = []
//   const values2 = []

//   for (let i = 0; i <= 18; i++) {
//     values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
//     values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
//   }
//   data2.datasets[0].data = values1
//   data2.datasets[1].data = values2
// }

setDefault1()
// setDefault2()
</script>

<style lang="scss" scoped>
@import '@/assets/styles/components/badge.scss';

.seller-resume {
  display: flex;
  flex-direction: column;

  &__info {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
    margin-bottom: 32px;
  }

  &__graphics {
    width: 100%;
    display: grid;
    grid-gap: 60px;
    padding: 24px 40px 40px;
    background: var(--white);
    border-radius: 16px;
  }
}

.seller-resume-graphic {
  display: flex;
  flex-direction: column;

  &__title {
    margin-bottom: 16px;
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__badges {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin: -4px;

    .badge {
      margin: 4px;
    }
  }

  &__chart {
    width: 100%;
    height: 420px;
    margin-top: 32px;
  }
}
</style>
