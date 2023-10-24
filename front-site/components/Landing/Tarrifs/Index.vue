<template>
  <div id="tarifs" class="tarrifs">
    <div class="container">
      <div class="tarrifs__box">
        <h2 class="tarrifs__title">
          Тарифы
        </h2>

        <div class="tarrifs__cards">
          <CommonSubscribeCard
            v-for="(item, i) in cards"
            :key="i"
            :item="item"
            class="tarrifs__card"
          />
        </div>

        <CommonContactsBlock
          title="Будем рады вашей обратной связи"
          primary-gray
          class="tarrifs__contacts"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const cards = [
  {
    type: 'trial',
    title: 'Базовый',
    text: 'Тариф для тех, кому только посмотреть. Максимальный функционал для бесплатного тарифа.',
    price: '0 ₽',
    textBtn: 'Начать с базового тарифа',
    list: [
      'Период анализа: 30 дней',
      'Ежедневное обновление',
      'Поиск и анализ товаров, категорий, брендов и продавцов',
      'Выгрузка аналитических отчетов в csv',
    ],
  },
  {
    type: 'premium',
    title: 'Продвинутый',
    text: 'Тариф для тех, кому интересны новые товары и ниши. Определите товар, который будет приносить наибольший доход.',
    price: '1 990 ₽',
    textBtn: 'Попробовать бесплатно',
    list: [
      'Подборка топ ниш',
      'Период анализа: 90 дней',
      'Ежедневное обновление',
      'Поиск и анализ товаров, категорий, брендов и продавцов',
      'Выгрузка аналитических отчетов в csv',
      '5 дней бесплатно, без привязки карты',
    ],
  },
]
</script>

<style lang="scss" scoped>
.tarrifs {
  &__box {
    display: flex;
    flex-direction: column;
    padding: 60px 0 48px;

    @include mq($bp-medium) {
      padding: 100px 0 60px;
    }
  }

  &__title {
    @include h2;

    margin-bottom: 32px;
    color: var(--blackMain);
    text-align: center;
  }

  &__cards {
    display: grid;
    grid-gap: 12px;
    justify-content: center;

    @include mq($bp-small) {
      grid-gap: 16px;
      grid-template-columns: repeat(2, minmax(350px, 416px));
    }
  }

  &__card {
    max-width: 320px;

    @include mq($bp-small) {
      max-width: 100%;
    }
  }

  &__contacts {
    margin-top: 60px;

    @include mq($bp-medium) {
      margin-top: 100px;
    }
  }
}
</style>
