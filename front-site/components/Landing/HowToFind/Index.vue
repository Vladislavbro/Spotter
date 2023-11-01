<template>
  <div id="opportunity" class="how-to-find">
    <div class="container">
      <div class="how-to-find__box">
        <div class="how-to-find__cards">
          <div class="card">
            <div class="card__content">
              <p class="card__title">
                Выбирайте из уже<br>отобранных ниш
              </p>
              <p class="card__description">
                Смотрите объем рынка, количество продавцов и количество товаров в с продажами. Используйте фильтры и сортировку для отбора ниш по интересующим вас критериям. Переходите на детальный анализ заинтересовавшей вас ниши.
              </p>
              <UIBaseButton
                text="Найти свою нишу"
                to="/lk"
              />
            </div>

            <div class="card__image">
              <img src="@/assets/images/landing/how-to-find/1.png" alt="">
            </div>
          </div>

          <div class="card">
            <div class="card__content">
              <p class="card__title">
                Смотрите детальную<br>аналитику по нише
              </p>
              <p class="card__description">
                В детальной аналитике вас ждем вкладка с анализом ниши и со сводкой по товарам. В детальной аналитике можно посмотреть почему ниша набрала такой рейтинг, лучшие товары по обороту, основные показатели и и историю их изменений
              </p>
              <UIBaseButton
                text="Изучить подробно"
                to="/lk"
              />
            </div>

            <div class="card__image">
              <img src="@/assets/images/landing/how-to-find/2.png" alt="">
            </div>
          </div>

          <div class="card">
            <div class="card__content">
              <p class="card__title">
                Выбирайте товары<br>для продажи
              </p>
              <p class="card__description">
                Переходите во вкладку со сводкой по товарам, изучайте какие товары пользуются наибольшим спросам и по какой цене продаются. Для более детального изучения товара или продавца можно перейти на их страницы с более подробным анализом.
              </p>
              <UIBaseButton
                text="Выбрать товар"
                to="/lk"
              />
            </div>

            <div class="card__image">
              <img src="@/assets/images/landing/how-to-find/3.png" alt="">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.how-to-find {
  color: var(--blackMain);
  background: #F2F2F4;
  overflow: hidden;

  &__box {
    display: flex;
    flex-direction: column;
    padding: 60px 0;

    @include mq($bp-medium) {
      padding: 100px 0;
    }
  }

  &__cards {
    width: 100%;

    display: grid;
    grid-gap: 20px;
  }
}

.card {
  width: 100%;

  display: grid;
  align-items: center;
  justify-content: space-between;
  grid-template-columns: 1fr;
  grid-gap: 40px;

  padding: 32px 16px 16px 16px;

  background: var(--white);
  border: 8px solid #E9E9EA;
  border-radius: 24px;

  @include mq($bp-medium) {
    grid-template-columns: minmax(300px, 500px) minmax(350px, 624px);
    grid-gap: 20px;

    padding: 24px 24px 24px 24px;
  }

  @include mq($bp-big) {
    padding: 24px 24px 24px 60px;
  }

  &__content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  &__title {
    margin-bottom: 12px;

    font-weight: 600;
    font-size: 22px;
    line-height: 26px;

    @include mq($bp-small) {
      margin-bottom: 20px;

      font-size: 36px;
      line-height: 44px;
    }
  }

  &__description {
    width: 100%;

    margin-bottom: 24px;

    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small) {
      margin-bottom: 32px;

      font-size: 15px;
      line-height: 22px;
    }

    @include mq($bp-medium) {
      max-width: 480px;
    }
  }

  &__image {
    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;
    overflow: hidden;
  }
}
</style>
