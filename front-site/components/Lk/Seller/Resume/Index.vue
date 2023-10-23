<template>
  <div class="seller-resume">
    <div class="seller-resume__info">
      <!-- <LkTableTypes /> -->

      <LkTableDate
        @change="changeDate"
      />
    </div>

    <div class="seller-resume__box">
      <div v-if="!isLoading" class="seller-resume__graphics">
        <div class="seller-resume__graphic seller-resume-graphic">
          <p class="seller-resume-graphic__title">
            Оборот и средний чек
          </p>
          <div class="seller-resume-graphic__badges">
            <span
              v-for="(item, i) in data.datasets"
              :key="i"
              class="badge"
            >
              {{ item.label }}:
              <span class="badge__value">
                {{ item.data.reduce((sum, a) => sum + a, 0).toLocaleString() }}
                {{ item.valueSuffix }}
              </span>
            </span>
            <!-- <span class="badge badge--purple">
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
            </span> -->
          </div>

          <div class="seller-resume-graphic__chart">
            <LkChart
              :data="data"
              :options="options"
            />
          </div>
        </div>
      </div>

      <div
        v-else
        class="seller-resume__loader"
      >
        <UILoader />
      </div>
    </div>
  </div>
</template>

<script setup>
import { sub } from 'date-fns'

const route = useRoute()

const { slug } = route.params

const day = ref(30)
const isLoading = ref(true)
// const isLoadingGraphs = ref(false)
const graphs = ref([])

const data = ref({
  labels: [],
  datasets: [
    {
      label: 'Цена',
      valueSuffix: '₽',
      borderColor: '#FF8F6D',
      pointBorderColor: '#FF8F6D',
      data: [],
    },
    {
      label: 'Оборот FBO',
      valueSuffix: '₽',
      borderColor: '#5480F2',
      pointBorderColor: '#5480F2',
      data: [],
    },
    {
      label: 'Оборот FBS',
      valueSuffix: '₽',
      borderColor: '#AE80EA',
      pointBorderColor: '#AE80EA',
      data: [],
    },
  ],
})

const options = {}

const setGraphicValues = () => {
  data.value.labels = []
  data.value.datasets[0].data = []
  data.value.datasets[1].data = []
  data.value.datasets[2].data = []

  graphs.value.forEach((item, i) => {
    data.value.labels.push(sub(new Date().setHours(0, 0, 0, 0), { days: i }))

    data.value.datasets[0].data.push(item.price)
    data.value.datasets[1].data.push(item.profit_fbo)
    data.value.datasets[2].data.push(item.profit_fbs)
  })
}

const changeDate = (data) => {
  day.value = data.day

  getData()
}

const getData = async () => {
  if (!slug) {
    return navigateTo('/lk')
  }

  isLoading.value = true

  const { data } = await useFetch(`/api/suppliers/${slug}`, {
    watch: false,
    query: {
      view: 'graphs',
      period: day.value,
    },
  })

  graphs.value = data?.value?.graphs || []
  setGraphicValues()

  isLoading.value = false
}

getData()
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

  &__loader {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 50px 0;
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
