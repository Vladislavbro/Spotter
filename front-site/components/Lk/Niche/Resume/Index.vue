<template>
  <div class="niche-resume">
    <template v-if="!isLoading && item">
      <div class="niche-resume__info">
        <LkTableTypes />

        <LkTableDate />
      </div>

      <LkNicheResumePerspective
        :item="item"
        :perspectives="perspectives"
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

const perspectives = ref([])

const setPerspective = () => {
  const priceAvgDiff = item?.value?.price_avg_diff || 0 // Стабильность среднего чека
  const monopoly = item?.value?.monopoly || 0
  const salesOrg = item?.value?.sales_org || 0 // Оценка потенциала органических продаж
  const salesAvg = item?.value?.sales_avg || 0 // Среднее количество продаж у товаров
  const productsCount = item?.value?.products_count || 0 // Конкурентный ассортимент

  const item1 = { title: '', text: '', score: 0, type: 'Продажи' }
  const item2 = { title: '', text: '', score: 0, type: 'Продажи' }
  const item3 = { title: '', text: '', score: 0, type: 'Продажи' }
  const item4 = { title: '', text: '', score: 0, type: 'Продажи' }

  const item5 = { title: '', text: '', score: 0, type: 'Рынок' }
  const item6 = { title: '', text: '', score: 0, type: 'Рынок' }
  const item7 = { title: '', text: '', score: 0, type: 'Рынок' }

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
}

const getData = async () => {
  isLoading.value = true
  const { data } = await useFetch(`/api/queries/search?query=${props.slug}&view=summary`)

  isLoading.value = false

  item.value = data?.value

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
