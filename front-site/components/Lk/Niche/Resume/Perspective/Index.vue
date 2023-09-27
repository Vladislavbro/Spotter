<template>
  <div class="perspective">
    <div class="perspective__header">
      <p class="perspective__title">
        Перспективность ниши
      </p>
      <button
        :class="['perspective__arrow', { 'perspective__arrow--open' : isOpen }]"
        @click.prevent="isOpen = !isOpen"
      >
        <UIBaseIcon name="lk/icon-arrow-left" />
      </button>
    </div>

    <div :class="['perspective__body', { 'perspective__body--open' : isOpen }]">
      <div class="perspective__content">
        <div class="perspective__aside">
          <div
            :class="[
              'perspective-point',
              { 'perspective-point--bad' : item.scoring <= 3 },
              { 'perspective-point--normal' : item.scoring > 3 && item.scoring <= 6 },
              { 'perspective-point--good' : item.scoring > 6 },
            ]"
          >
            <p class="perspective-point__title">
              {{ item.scoring }}/10
            </p>
            <div class="perspective-point__desc">
              {{ getPerspectiveTitle }}
            </div>
          </div>

          <div class="perspective-stats">
            <p class="perspective-stats__title">
              Статистика ниши
            </p>
            <div class="perspective-stats__list">
              <div class="perspective-stats-item perspective-stats-item--purple">
                <div class="perspective-stats-item__header">
                  <p class="perspective-stats-item__label">
                    Продажи
                  </p>
                  <span class="perspective-stats-item__value">
                    {{ stats.sales > 0 ? stats.sales : 0 }}/4
                  </span>
                </div>
                <div class="perspective-stats-item__progress">
                  <div
                    :style="`width: ${100 / 4 * (stats.sales > 0 ? stats.sales : 0)}%`"
                    class="perspective-stats-item__progress-line"
                  />
                </div>
              </div>
              <div class="perspective-stats-item perspective-stats-item--blue">
                <div class="perspective-stats-item__header">
                  <p class="perspective-stats-item__label">
                    Рынок
                  </p>
                  <span class="perspective-stats-item__value">
                    {{ stats.shop > 0 ? stats.shop : 0 }}/3
                  </span>
                </div>
                <div class="perspective-stats-item__progress">
                  <div
                    :style="`width: ${100 / 3 * (stats.shop > 0 ? stats.shop : 0)}%`"
                    class="perspective-stats-item__progress-line"
                  />
                </div>
              </div>
              <div class="perspective-stats-item perspective-stats-item--orange">
                <div class="perspective-stats-item__header">
                  <p class="perspective-stats-item__label">
                    Конкуренция
                  </p>
                  <span class="perspective-stats-item__value">
                    {{ stats.conc > 0 ? stats.conc : 0 }}/5
                  </span>
                </div>
                <div class="perspective-stats-item__progress">
                  <div
                    :style="`width: ${100 / 5 * (stats.conc > 0 ? stats.conc : 0)}%`"
                    class="perspective-stats-item__progress-line"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="perspective__cards">
          <LkNicheResumePerspectiveCard
            v-for="(card, i) in perspectives"
            :key="i"
            :item="card"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stats: {
    type: Object,
    default: () => ({}),
  },
  item: {
    type: Object,
    default: () => ({}),
  },
  perspectives: {
    type: Array,
    default: () => ([]),
  },
})

const isOpen = ref(true)

// const perspectives = [
//   { title: 'Стабильный средний чек', text: 'Стабильный чек означает здоровую конкуренцию, без демпинга', type: 'Продажи' },
//   { title: 'Монополия в нише исключена', text: 'Соотношение спроса и предложения в нише идеально, если попасть в ТОП 10, можно забрать на себя основные продажи', type: 'Продажи' },
//   { title: 'Высокий потенциал органических продаж', text: 'В нише большая часть товаров имеет продажи, оптимизированная карточка (SEO, Rich - контент), точно получит продажи', type: 'Продажи' },
//   { title: 'Активный рост продаж', text: 'Среднесуточный оборот активно растет - это поможет вашим продажам. Обратите внимание на графики, чтобы понять, тренд это или временная распродажа', type: 'Рынок' },
//   { title: 'Переполненность конкурентным ассортиментом', text: 'Конкуренция высокая, вам понадобятся все методы продвижения: оптимизировать карточку (SEO, Rich контент) и продвижение в ТОП', type: 'Рынок' },
//   { title: 'Огромный рынок', text: 'Попробуйте конкретизировать свой запрос и проанализировать определенную нишу, а не направление. Например, вместо "подушка" введите "подушка берем", чтобы анализировать подушки для беременных', type: 'Рынок' },
//   { title: 'Рост конкуренции отсутствует', text: 'Конкуренция держится на одном уровне - это отличный показатель', type: 'Конкуренция' },
// ]

const getPerspectiveTitle = computed(() => {
  const score = props.item?.scoring || 0
  if (score <= 3) {
    return 'Низкая перспективность ниши'
  } else if (score > 3 && score <= 6) {
    return 'Средняя перспективность ниши'
  } else if (score > 6) {
    return 'Высокая перспективность ниши'
  }
})
</script>

<style lang="scss" scoped>
.perspective {
  display: flex;
  flex-direction: column;
  padding: 28px 40px 0 28px;
  background: var(--white);
  border-radius: 16px;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 24px;
    border-bottom: 1px solid #E2E2E7;
  }

  &__title {
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--white);
    box-shadow: 0px 2px 6px rgba(44, 48, 64, 0.2);
    border-radius: 4px;

    ::v-deep(.ui-icon) {
      transform: rotate(90deg);
      transition: transform 0.3s;

      svg {
        width: 20px;
        height: 20px;
      }
    }

    &--open {
      ::v-deep(.ui-icon) {
        transform: rotate(-90deg);
      }
    }
  }

  &__body {
    max-height: 570px;
    overflow-y: auto;
    margin-right: -32px;
    padding-right: 24px;
    scrollbar-width: thin;
    scrollbar-color: #D9D9E0 #F3F4F5;
    transition: max-height 0.3s;

    &--open {
      max-height: 9999px;
    }

    &::-webkit-scrollbar {
      width: 8px;
    }
    &::-webkit-scrollbar-track {
      background: #F3F4F5;
    }
    &::-webkit-scrollbar-thumb {
      background-color: #D9D9E0;
      border-radius: 16px;
    }
  }

  &__content {
    display: grid;
    grid-gap: 30px;
    grid-template-columns: 350px 1fr;
    justify-content: flex-start;
    align-items: flex-start;
    padding-top: 32px;
    padding-bottom: 40px;
  }

  &__aside {
    display: grid;
    grid-gap: 20px;
  }

  &__cards {
    display: grid;
    grid-gap: 12px;
    grid-template-columns: repeat(3, 1fr);
  }
}

.perspective-point {
  display: grid;
  grid-gap: 8px;
  width: 100%;
  padding: 28px;
  color: var(--white);
  font-weight: 500;
  border-radius: 12px;

  &--bad {
    background: linear-gradient(90deg, #E05440 0%, #D93333 100%);
  }

  &--normal {
    background: linear-gradient(90deg, #F9C747 0%, #FEC350 100%);
  }

  &--good {
    background: linear-gradient(90deg, #3EB87B 0%, #049669 100%);
  }

  &__title {
    font-size: 80px;
    line-height: 80px;
  }

  &__desc {
    font-size: 15px;
    line-height: 18px;
  }
}

.perspective-stats {
  display: grid;
  grid-gap: 24px;
  padding: 28px 28px 68px;
  border: 1px dashed #D9D9E0;
  border-radius: 12px;

  &__title {
    font-weight: 600;
    font-size: 22px;
    line-height: 28px;
  }

  &__list {
    display: grid;
    grid-gap: 20px;
  }
}

.perspective-stats-item {
  display: grid;
  grid-gap: 6px;
  font-weight: 500;

  &--purple {
    .perspective-stats-item {
      &__value {
        color: #8557E5;
        background: #F3EAFF;
      }
      &__progress-line {
        background: #8557E5;
      }
    }
  }

  &--blue {
    .perspective-stats-item {
      &__value {
        color: #5076FE;
        background: #E3EBFF;
      }
      &__progress-line {
        background: #5076FE;
      }
    }
  }

  &--orange {
    .perspective-stats-item {
      &__value {
        color: #F57256;
        background: #FFEBE7;
      }
      &__progress-line {
        background: #F57256;
      }
    }
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__title {
    font-size: 15px;
    line-height: 18px;
  }

  &__value {
    padding: 4px 8px;
    font-size: 14px;
    line-height: 16px;
    border-radius: 60px;
  }

  &__progress {
    position: relative;
    width: 100%;
    height: 20px;
    background: #E3EBFF;
    border-radius: 60px;

    &-line {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      width: 0%;
      border-radius: 60px;
    }
  }
}
</style>
