<template>
  <div class="subscribes">
    <div class="container-lk container-lk--profile">
      <div class="subscribes__box">
        <h1 class="subscribes__title">
          Тарифы
        </h1>

        <div class="subscribes__cards">
          <CommonSubscribeCard
            v-for="(item, i) in cards"
            :key="i"
            :item="item"
            is-lk
            class="subscribes__card"
            @subscribe="subscribe"
          />
        </div>

        <CommonContactsBlock
          title="Будем рады вашей обратной связи"
          class="subscribes__contacts"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'lk',
})

const cards = [
  {
    type: 'trial',
    title: 'Базовый',
    text: 'Тариф для тех, кому только посмотреть. Максимальный функционал для бесплатного тарифа.',
    price: '0 ₽',
    textBtn: 'Начать с базового тарифа',
    list: [
      'Кол-во запросов: 20',
      'Поиск и анализ товаров, категорий, брендов и продавцов',
      'Выгрузка аналитических отчетов в csv',
    ],
  },
  {
    type: 'premium',
    title: 'Продвинутый',
    text: 'Тариф для тех, кому интересны новые товары и ниши. Определите товар, который будет приносить наибольший доход.',
    price: '1 990 ₽',
    textBtn: 'Попробовать',
    list: [
      'Кол-во запросов: без ограничений',
      'Поиск и анализ товаров, категорий, брендов и продавцов',
      'Выгрузка аналитических отчетов в csv',
      'Подборка топ ниш',
    ],
  },
]

const subscribe = async (obj) => {
  // console.log('data', obj)

  const { data, error } = await useFetch('/api/order', {
    method: 'post',
    body: {
      amount: 0,
      subscribe_type: obj,
    },
    headers: useHeaderToken(),
  })

  // console.log('data', data)
  // console.log('error', error)
}
</script>

<style lang="scss" scoped>
.subscribes {
  font-family: 'Hauora';

  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 60px;
  }

  &__title {
    margin-bottom: 32px;
    font-weight: 600;
    font-size: 36px;
    line-height: 44px;
  }

  &__cards {
    display: grid;
    grid-gap: 16px;
    grid-template-columns: repeat(2, 380px);
  }

  &__contacts {
    margin-top: 80px;
  }
}
</style>
