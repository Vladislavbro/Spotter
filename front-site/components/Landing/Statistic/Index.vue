<template>
  <div class="statistic">
    <div class="container">
      <div class="statistic__box">
        <h2 class="statistic__title">
          Статистика Wildberries
        </h2>

        <div class="statistic__cards">
          <div class="statistic__card card">
            <div class="card__content">
              <p class="card__title">
                85% карточек товаров на&nbsp;Wildberries не&nbsp;продаются
              </p>
            </div>
          </div>

          <div class="statistic__card card card_black">
            <div class="card__content">
              <p class="card__title">
                70% продавцов на Wildberries зарабатывают меньше 20 000 руб. в месяц или работают в минус
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.statistic {
  &__box {
    display: flex;
    flex-direction: column;
    padding: 60px 0;

    @include mq($bp-medium) {
      padding: 100px 0;
    }
  }

  &__title {
    @include h2;

    width: 100%;
    margin-bottom: 28px;
    color: var(--blackMain);
    text-align: center;

    @include mq($bp-small) {
      margin-bottom: 48px;
    }
  }

  &__cards {
    display: grid;
    grid-gap: 8px;

    @include mq($bp-small-medium) {
      grid-gap: 16px;
      grid-template-columns: repeat(2, 1fr);
    }
  }
}

.card {
  height: 220px;
  padding: 24px 16px;
  border-radius: 12px;
  background: var(--purple) url('@/assets/icons/landing/statistic/cards.svg')no-repeat 100% calc(100% - 10px);
  background-size: 166px;

  @include mq($bp-small) {
    height: 380px;
    padding: 40px;
    background-size: auto;
    border-radius: 24px;
  }

  &_black {
    background: var(--blackMain) url('@/assets/icons/landing/statistic/sales.svg')no-repeat calc(100% - 17px) calc(100% - 13px);
    background-size: 136px;

    @include mq($bp-small) {
      background-size: auto;
    }

    .card {
      &__content {
        max-width: 220px;

        @include mq($bp-small) {
          max-width: 390px;
        }
      }

      &__title {
        @include mq($bp-small) {
          text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
        }
      }
    }
  }

  &__content {
    display: flex;
    flex-direction: column;

    @include mq($bp-small) {
      max-width: 280px;
    }
  }

  &__title {
    font-weight: 500;
    font-size: 15px;
    line-height: 20px;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 30px;
    }
  }
}
</style>
