<template>
  <div :class="`resume-stats-card resume-stats-card--${item.type}`">
    <div class="resume-stats-card__header">
      <p class="resume-stats-card__title">
        {{ item.title }}
      </p>

      <LkTooltip
        is-white
        direction="bottom"
        text="Упущенная продавцами выручка (Lost profit), которая возникла из-за того, что продавцы вовремя не пополнили товары для заказов. Значение формируется на основании данных о продажах предыдущего периода"
        class="resume-stats-card__tooltip"
      />
    </div>

    <div class="resume-stats-card__body">
      <div class="resume-stats-card__arrow">
        <UIBaseIcon name="lk/icon-sort-arrow-down" />
      </div>
      <p class="resume-stats-card__price">
        {{ item.price }}
        <span
          v-if="+item.price_percent"
          class="resume-stats-card__price-percent"
        >
          ({{ item.price_percent }})%
        </span>
      </p>
      <!-- <p
        v-if="item.diff || item.percent"
        class="resume-stats-card__percent"
      >
        {{ item.diff ? item.diff : '' }} {{ item.percent ? `(${item.percent}%)` : '' }}
      </p> -->
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})
</script>

<style lang="scss" scoped>
.resume-stats-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 225px;
  padding: 24px 12px 24px 16px;
  background: #2D2D34;
  border-radius: 8px;

  &--up {
    .resume-stats-card {
      &__arrow {
        transform: rotate(180deg);

        ::v-deep(.ui-icon) {
          path {
            fill: #98E012;
          }
        }
      }

      &__percent {
        color: #98E012;
      }
    }
  }

  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  &__title {
    margin-right: 8px;
    font-weight: 500;
    font-size: 16px;
    line-height: 22px;
  }

  &__tooltip {
    ::v-deep(.ui-icon) {
      svg {
        width: 24px;
        height: 24px;
      }

      path {
        fill: #9D9DA5;
      }
    }
  }

  &__body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  &__arrow {
    margin-bottom: 20px;

    ::v-deep(.ui-icon) {
      svg {
        width: 20px;
        height: 20px;
      }

      path {
        fill: #F04B55;
      }
    }
  }

  &__price {
    display: flex;
    align-items: baseline;
    grid-gap: 4px;

    margin-bottom: 8px;

    font-size: 20px;
    line-height: 24px;
  }

  &__price-percent {
    color: var(--grayLight);
    font-size: 13px;
    line-height: 16px;
  }

  &__percent {
    font-size: 14px;
    line-height: 18px;
    color: #F04B55;
  }
}
</style>
