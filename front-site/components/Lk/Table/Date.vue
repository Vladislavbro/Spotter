<template>
  <div :class="['lk-date', { 'lk-date--calendar': calendarOnly }]">
    <div class="lk-date__calendar">
      <UIBaseIcon
        name="lk/icon-calendar"
      />
      14.02.2022 - 21.02.2022
    </div>

    <div
      v-if="!calendarOnly"
      class="lk-date__days"
    >
      <button
        v-for="(item, i) in days"
        :key="i"
        :class="['lk-date__day', { 'lk-date__day--active' : day === item.value }]"
        @click.prevent="day = item.value"
      >
        {{ item.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  calendarOnly: {
    type: Boolean,
    default: false,
  },
})

const days = [
  { label: '7 дней', value: 7 },
  { label: '14 дней', value: 14 },
  { label: 'месяц', value: 30 },
]

const day = ref(30)
</script>

<style lang="scss" scoped>
.lk-date {
  display: grid;
  align-items: center;
  grid-template-columns: repeat(2, auto);
  grid-gap: 12px;
  font-weight: 500;
  font-size: 15px;
  line-height: 18px;

  &--calendar {
    grid-gap: 0;
  }

  &__calendar {
    display: grid;
    align-items: center;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    height: 46px;
    padding: 0 20px;
    background: var(--white);
    border: 1px solid #E2E2E7;
    border-radius: 8px;
    cursor: pointer;

    &:hover {
      background: #F3F4F5;
    }
  }

  &__days {
    display: flex;
    align-items: center;
    padding: 4px;
    background: #E9EAEC;
    border-radius: 8px;
  }

  &__day {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 38px;
    padding: 0 20px;
    border-radius: 4px;

    &:hover:not(.lk-date__day--active) {
      background: #F3F4F5;
    }

    &--active {
      color: var(--white);
      background: #8557E5;
      box-shadow: 0px 2px 6px rgba(42, 46, 59, 0.24);
    }
  }
}
</style>
