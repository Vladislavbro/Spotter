<template>
  <div class="resume-graphic">
    <div class="resume-graphic__header">
      <p class="resume-graphic__title">
        Изменения показателей
      </p>

      <!-- <LkTableDate
        calendar-only
      /> -->
    </div>

    <template v-if="!isLoading">
      <div class="resume-graphic__checkboxes">
        <label
          v-for="(item, i) in data.datasets"
          :key="i"
          :class="['resume-graphic__checkbox resume-graphic-checkbox', { 'resume-graphic-checkbox--checked' : !item.hidden }]"
        >
          <div class="resume-graphic-checkbox__content">
            <p class="resume-graphic-checkbox__label">
              {{ item.label }}
            </p>
            <p class="resume-graphic-checkbox__count">
              {{ item.data.reduce((sum, a) => sum + a, 0).toLocaleString() }}
              {{ item.valueSuffix }}
            </p>
          </div>
          <input
            v-model="item.hidden"
            type="checkbox"
            @change="changeCheckbox"
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
    </template>
    <div
      v-else
      class="resume-graphic__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
import { sub } from 'date-fns'

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

const graphs = ref([])
const isLoading = ref(true)

watch(() => props.fb, () => {
  getData()
})

watch(() => props.day, () => {
  getData()
})

const data = ref({
  labels: [],
  datasets: [
    {
      label: 'Оборот',
      valueSuffix: '₽',
      borderColor: '#FF8F6D',
      pointBorderColor: '#FF8F6D',
      data: [],
      hidden: false,
    },
    {
      label: 'Средний чек',
      valueSuffix: '₽',
      borderColor: '#F488D7',
      pointBorderColor: '#F488D7',
      data: [],
      hidden: false,
    },
    {
      label: 'Продажи',
      valueSuffix: 'шт.',
      borderColor: '#AE80EA',
      pointBorderColor: '#AE80EA',
      data: [],
      hidden: false,
    },
    {
      label: 'Кол-во товаров',
      valueSuffix: 'шт.',
      borderColor: '#5480F2',
      pointBorderColor: '#5480F2',
      data: [],
      hidden: false,
    },
    {
      label: 'Продавцы',
      valueSuffix: 'шт.',
      borderColor: '#6DC68B',
      pointBorderColor: '#6DC68B',
      data: [],
      hidden: false,
    },
    {
      label: 'Бренды',
      valueSuffix: 'шт.',
      borderColor: '#F4D037',
      pointBorderColor: '#F4D037',
      data: [],
      hidden: false,
    },
  ],
})

const options = {}

// const setDefault = () => {
//   const labels = []
//   for (let i = 10; i <= 28; i++) {
//     labels.push(new Date(`2023-02-${i} 00:00:00`).getTime())
//   }
//   data.labels = labels

//   const values1 = []
//   const values2 = []
//   const values3 = []
//   const values4 = []
//   const values5 = []
//   const values6 = []

//   for (let i = 0; i <= 18; i++) {
//     values1.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
//     values2.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
//     values3.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
//     values4.push(Math.floor(Math.random() * (135000 - 75000 + 1)) + 75000)
//     values5.push(Math.floor(Math.random() * (115000 - 10000 + 1)) + 10000)
//     values6.push(Math.floor(Math.random() * (100000 - 20000 + 1)) + 20000)
//   }
//   data.datasets[0].data = values1
//   data.datasets[1].data = values2
//   data.datasets[2].data = values3
//   data.datasets[3].data = values4
//   data.datasets[4].data = values5
//   data.datasets[5].data = values6
// }

// setDefault()

const setGraphicValues = () => {
  graphs.value.forEach((item, i) => {
    data.value.labels.push(sub(new Date().setHours(0, 0, 0, 0), { days: i }))

    data.value.datasets[0].data.push(item.profit)
    data.value.datasets[1].data.push(item.price)
    data.value.datasets[2].data.push(item.sales)
    data.value.datasets[3].data.push(item.products)
    data.value.datasets[4].data.push(item.sellers)
    data.value.datasets[5].data.push(item.brands)
  })
}

const getData = async () => {
  isLoading.value = true
  graphs.value = []

  const params = {
    fb: props.fb,
  }

  if (props.day) {
    params.period = props.day
  }

  const { data } = await useFetch(`/api/queries/search?query=${slug}&view=graphs`, {
    watch: false,
    params,
  })

  graphs.value = data?.value?.graphs || []
  setGraphicValues()

  isLoading.value = false
}

getData()
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

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
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
