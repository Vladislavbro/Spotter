<template>
  <div class="niche-resume">
    <template v-if="!isLoadingPage">
      <div class="niche-resume__info">
        <LkTableTypes
          :value="fb"
          @change="changeType"
        />

        <LkTableDate
          @change="changeDate"
        />
      </div>

      <template v-if="!isLoading">
        <LkNicheResumePerspective
          :stats="stats"
          :item="item"
          :perspectives="perspectives"
          class="niche-resume__perspective"
        />

        <LkNicheResumeTopItems
          :items="topItems"
          :type="fb"
          :day="day"
          class="niche-resume__top-items"
        />

        <LkNicheResumeStats
          :item="item"
          class="niche-resume__stats"
        />

        <LkNicheResumeGraphic />
      </template>
    </template>
    <div
      v-else
      class="niche-resume__loader"
    >
      <UILoader />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  slug: {
    type: String,
    default: '',
  },
})

const isLoadingPage = ref(true)
const isLoading = ref(false)

const item = ref(null)
const topItems = ref([])
const fb = ref('fbo')
const day = ref(30)
const date = ref(null)

const perspectives = ref([])

const stats = computed(() => {
  const arr = {
    sales: 0,
    shop: 0,
    conc: 0,
  }

  perspectives.value.forEach((item) => {
    arr[item.type] += item.score
  })

  return arr
})

const setPerspective = () => {
  const priceAvgDiff = item?.value?.price_avg_diff || 0 // Стабильность среднего чека
  const monopoly = item?.value?.monopoly || 0
  const salesOrg = item?.value?.sales_org || 0 // Оценка потенциала органических продаж
  const salesAvg = item?.value?.sales_avg || 0 // Среднее количество продаж у товаров

  const productsCount = item?.value?.products_count || 0 // Конкурентный ассортимент
  const salesTrend = item?.value?.sales_trend || 0 // Оценка тренда продаж
  const profit = item?.value?.profit || 0 // Объем рынка

  const suppliers = item?.value?.suppliers || 0 // Востребованность ниши
  const volume = item?.value?.volume || 0 // Объем рынка (динамика)
  const profitLost = item?.value?.profit_lost || 0 // LP - Упущенная выручка в нише
  const profitTopSupDiff = item?.value?.profit_top_sup_diff || 0 // Объем рынка у топ 10 (динамика)
  const productSoldedDiff = item?.value?.product_solded_diff || 0 // SPP - Процент товаров с продажами (динамика)

  const salesSpeedAvg = item?.value?.sales_speed_avg || 0 // Средняя скорость продаж
  const supplierProfitAvg = item?.value?.supplier_profit_avg || 0 // Средний оборот на продавца
  const supplierSoldDiff = item?.value?.supplier_sold_diff || 0 // SPS - процент продавцов с продажами

  const item1 = { title: '', text: '', score: 0, type: 'sales', type_text: 'Продажи' }
  const item2 = { title: '', text: '', score: 0, type: 'sales', type_text: 'Продажи' }
  const item3 = { title: '', text: '', score: 0, type: 'sales', type_text: 'Продажи' }
  const item4 = { title: '', text: '', score: 0, type: 'sales', type_text: 'Продажи' }

  const item5 = { title: '', text: '', score: 0, type: 'shop', type_text: 'Рынок' }
  const item6 = { title: '', text: '', score: 0, type: 'shop', type_text: 'Рынок' }
  const item7 = { title: '', text: '', score: 0, type: 'shop', type_text: 'Рынок' }

  const item8 = { title: '', text: '', score: 0, type: 'conc', type_text: 'Конкуренция' }
  const item9 = { title: '', text: '', score: 0, type: 'conc', type_text: 'Конкуренция' }
  const item10 = { title: '', text: '', score: 0, type: 'conc', type_text: 'Конкуренция' }
  const item11 = { title: '', text: '', score: 0, type: 'conc', type_text: 'Конкуренция' }
  const item12 = { title: '', text: '', score: 0, type: 'conc', type_text: 'Конкуренция' }

  const item13 = { title: '', text: '', score: 0, type: '', type_text: 'Доп показатели' }
  const item14 = { title: '', text: '', score: 0, type: '', type_text: 'Доп показатели' }
  const item15 = { title: '', text: '', score: 0, type: '', type_text: 'Доп показатели' }

  if (priceAvgDiff > 1.01) {
    item1.title = 'Средний чек растет'
    item1.text = 'Повышение среднего чека означает, что в нише спрос больше предложения - это хорошо, если вы найдете нужные товары'
    item1.score = 0
  } else if (priceAvgDiff <= 1.01 && priceAvgDiff >= 0.9) {
    item1.title = 'Стабильный средний чек'
    item1.text = 'Стабильный чек означает здоровую конкуренцию, без демпинга'
    item1.score = 1
  } else if (priceAvgDiff < 0.9) {
    item1.title = 'Средний чек падает'
    item1.text = 'Падение среднего чека означает падение спроса или демпинг в нише'
    item1.score = -1
  }
  perspectives.value.push(item1)

  if (monopoly > 0.5) {
    item2.title = 'Сильная монополия в нише'
    item2.text = 'Лидеры забирают основную долю продаж, чтобы делать хороший оборот, необходимо продвинуться в ТОП 10'
    item2.score = -1
  } else if (monopoly >= 0.25 && monopoly <= 0.5) {
    item2.title = 'Есть признаки монополии в нише'
    item2.text = 'Часть лидеров в нише занимаются продвижением, постарайтесь попасть в ТОП 10, чтобы делить с ними основную долю продаж'
    item2.score = 0
  } else if (monopoly < 0.25) {
    item2.title = 'Хорошо распределенные продажи'
    item2.text = 'Покупатели не выбирают конкретный бренд или продавца, это пример здоровой ниши, вы можете заходить даже с "no name" товаром'
    item2.score = 1
  }
  perspectives.value.push(item2)

  if (salesOrg >= 0.5) {
    item3.title = 'Высокий потенциал органических продаж'
    item3.text = 'В нише большая часть товаров имеет продажи, оптимизированная карточка (SEO, Rich - контент), точно получит продажи'
    item3.score = 1
  } else if (salesOrg >= 0.3 && salesOrg < 0.5) {
    item3.title = 'Средний потенциал органических продаж'
    item3.text = 'Чтобы получить органические продажи, необходимо оптимизировать карточку (SEO, Rich - контент) и запустить на нее рекламу'
    item3.score = 0
  } else if (salesOrg < 0.3) {
    item3.title = 'Низкий потенциал органических продаж'
    item3.text = 'Для продаж в данной нише, продвижение обязательно. Начните с SEO - оптимизации карточки товара и продающего Rich - контента'
    item3.score = -1
  }
  perspectives.value.push(item3)

  if (salesAvg >= 30) {
    item4.title = 'Высокие продажи у товаров в нише'
    item4.text = 'Это хорошо, вы можете сфокусироваться на 3-4 товарах стабильных товарах для покорения ниши'
    item4.score = 1
  } else if (salesAvg >= 12 && salesAvg < 30) {
    item4.title = 'Средний уровень продаж у товаров в нише'
    item4.text = 'Будьте готовы отбирать 10-15 товаров для хороших продаж в нише'
    item4.score = 1
  } else if (salesAvg < 12) {
    item4.title = ' Низкий уровень продаж у товаров'
    item4.text = 'Пробиться в продажи будет трудно, проверьте наличие монополии внише'
    item4.score = 0
  }
  perspectives.value.push(item4)

  if (productsCount < 1000) {
    item5.title = 'Малый конкурентный ассортимент'
    item5.text = 'Про эту нишу сейчас практически никто не знает, а вы ее нашли! Если есть признаки роста рынка, стоит заходить сюда со своим товаром'
    item5.score = 1
  } else if (productsCount >= 1000 && productsCount <= 2000) {
    item5.title = 'Средний конкурентный ассортимент'
    item5.text = 'Количество товаров говорит о средней конкуренции, однако ниша не перегрета предложением'
    item5.score = 0
  } else if (productsCount > 2000) {
    item5.title = 'Большой конкурентный ассортимент'
    item5.text = 'Пробиться в топ выдачи будет сложно'
    item5.score = -1
  }
  perspectives.value.push(item5)

  if (salesTrend > 1.01) {
    item6.title = 'Активный рост продаж'
    item6.text = 'Среднесуточный оборот активно растет - это поможет вашим продажам. Обратите внимание на графики, чтобы понять, тренд это или временная распродажа'
    item6.score = 1
  } else if (salesTrend <= 1.01 && salesTrend >= 0.9) {
    item6.title = 'Стабильный спрос'
    item6.text = 'Продажи стабильны, несмотря на колебания, можно заходить и не опасаться резкого обвала рынка'
    item6.score = 0
  } else if (salesTrend < 0.9) {
    item6.title = 'Падение продаж'
    item6.text = 'В нише падение продаж, возможно, стоит обратиться к другой нише'
    item6.score = -1
  }
  perspectives.value.push(item6)

  if (profit < 5000000) {
    item7.title = 'Микрорынок'
    item7.text = 'Эта ниша не способна принести вам хороших продаж, рекомендуем поискать еще'
    item7.score = -1
  } else if (profit >= 5000000 && profit < 10000000) {
    item7.title = 'Средний рынок'
    item7.text = 'Объем рынка на хорошем уровне'
    item7.score = 1
  } else if (profit >= 10000000 && profit <= 100000000) {
    item7.title = 'Крупный рынок'
    item7.text = 'Если это узконаправленная ниша, она точно представляет интерес'
    item7.score = 1
  } else if (profit > 100000000) {
    item7.title = 'Огромный рынок'
    item7.text = 'Возможно, стоит конкретизировать свой запрос, чтобы анализировать определенную нишу, а не направление. Например, вместо "подушка" введите "подушка для беременных", чтобы анализировать именно подушки для беременных'
    item7.score = -5
  }
  perspectives.value.push(item7)

  if (suppliers > 1.01) {
    item8.title = 'Растущая конкуренция'
    item8.text = 'Ниша востребована, поэтому туда заходят все больше продавцов, вы можете стать одним из них'
    item8.score = 0
  } else if (suppliers <= 1.01 && suppliers >= 0.9) {
    item8.title = 'Рост конкуренции отсутствует'
    item8.text = 'Конкуренция держится на одном уровне - это отличный показатель'
    item8.score = 1
  } else if (suppliers < 0.9) {
    item8.title = 'Конкуренция падает'
    item8.text = 'Продавцы уходят из этой ниши - возможно, есть проблемы со спросом или с товаром'
    item8.score = -1
  }
  perspectives.value.push(item8)

  if (volume > 1.01) {
    item9.title = 'Объем рынка (динамика)'
    item9.text = ''
    item9.score = 1
  } else if (volume <= 1.01 && volume >= 0.9) {
    item9.title = 'Объем рынка (динамика)'
    item9.text = ''
    item9.score = 0
  } else if (volume < 0.9) {
    item9.title = 'Объем рынка (динамика)'
    item9.text = ''
    item9.score = -1
  }
  perspectives.value.push(item9)

  const profitPercent = profit / 100
  if (profitLost <= profitPercent * 10) {
    item10.title = 'LP - Упущенная выручка в нише'
    item10.text = ''
    item10.score = -1
  } else if (profitLost > profitPercent * 10 && profitLost <= profitPercent * 20) {
    item10.title = 'LP - Упущенная выручка в нише'
    item10.text = ''
    item10.score = 0
  } else if (profitLost > profitPercent * 20) {
    item10.title = 'LP - Упущенная выручка в нише'
    item10.text = ''
    item10.score = 1
  }
  perspectives.value.push(item10)

  if (profitTopSupDiff > 1.01) {
    item11.title = 'Объем рынка у топ 10 (динамика)'
    item11.text = ''
    item11.score = -1
  } else if (profitTopSupDiff <= 1.01 && productSoldedDiff >= 0.9) {
    item11.title = 'Объем рынка у топ 10 (динамика)'
    item11.text = ''
    item11.score = 0
  } else if (profitTopSupDiff < 0.9) {
    item11.title = 'Объем рынка у топ 10 (динамика)'
    item11.text = ''
    item11.score = 0
  }
  perspectives.value.push(item11)

  if (productSoldedDiff > 1.01) {
    item12.title = 'SPP - Процент товаров с продажами (динамика)'
    item12.text = ''
    item12.score = 1
  } else if (productSoldedDiff <= 1.01 && productSoldedDiff >= 0.9) {
    item12.title = 'SPP - Процент товаров с продажами (динамика)'
    item12.text = ''
    item12.score = 0
  } else if (productSoldedDiff < 0.9) {
    item12.title = 'SPP - Процент товаров с продажами (динамика)'
    item12.text = ''
    item12.score = -1
  }
  perspectives.value.push(item12)

  if (salesSpeedAvg >= 1) {
    item13.title = 'Средняя скорость продаж'
    item13.text = ''
    item13.score = 1
  } else if (salesSpeedAvg >= 0.3 && salesSpeedAvg < 1) {
    item13.title = 'Средняя скорость продаж'
    item13.text = ''
    item13.score = 0
  } else if (salesSpeedAvg < 0.3) {
    item13.title = 'Средняя скорость продаж'
    item13.text = ''
    item13.score = -1
  }
  perspectives.value.push(item13)

  if (supplierProfitAvg >= 100000) {
    item14.title = 'Средний оборот на продавца'
    item14.text = ''
    item14.score = 1
  } else if (supplierProfitAvg >= 20000 && supplierProfitAvg < 100000) {
    item14.title = 'Средний оборот на продавца'
    item14.text = ''
    item14.score = 0
  } else if (supplierProfitAvg < 20000) {
    item14.title = 'Средний оборот на продавца'
    item14.text = ''
    item14.score = -1
  }
  perspectives.value.push(item14)

  if (supplierSoldDiff >= 0.5) {
    item15.title = 'SPS - процент продавцов с продажами'
    item15.text = ''
    item15.score = 1
  } else if (supplierSoldDiff >= 0.2 && supplierSoldDiff < 0.5) {
    item15.title = 'SPS - процент продавцов с продажами'
    item15.text = ''
    item15.score = 0
  } else if (supplierSoldDiff < 0.2) {
    item15.title = 'SPS - процент продавцов с продажами'
    item15.text = ''
    item15.score = -1
  }
  perspectives.value.push(item15)
}

const changeType = (value) => {
  item.value = null
  topItems.value = []
  perspectives.value = []
  fb.value = value

  getData()
}

const changeDate = (data) => {
  item.value = null
  topItems.value = []
  perspectives.value = []
  day.value = data.day
  date.value = data.date

  getData()
}

const getData = async () => {
  isLoading.value = true

  const params = {
    output: 'json',
    fb: fb.value,
  }

  if (day.value) {
    params.period = day.value
  }

  if (date.value) {
    params.dateTo = date.value
  }

  const { data } = await useFetch(`/api/queries/search?query=${props.slug}&view=summary`, {
    watch: false,
    params,
  })

  const productsQuery = await useFetch(`/api/queries/search?query=${props.slug}&view=products`, {
    watch: false,
    params: {
      ...params,
      sort: `profit_${day.value}_${fb.value}`,
      direction: 'desc',
      per_page: 5,
    },
  })

  isLoading.value = false
  isLoadingPage.value = false

  item.value = data?.value
  topItems.value = productsQuery?.data?.value?.items || []

  setPerspective()
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
