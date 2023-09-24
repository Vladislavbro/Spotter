<template>
  <div :class="['lk-date', { 'lk-date--calendar': calendarOnly }]">
    <VueDatePicker
      v-model="date"
      range
      multi-calendars="3"
      :month-change-on-scroll="false"
      :clearable="false"
      format="dd.MM.yyyy"
      :enable-time-picker="false"
      locale="ru"
      input-class-name="lk-date-calendar__input"
      class="lk-date-calendar"
    />

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
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

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

const date = ref(null)
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
    transition: background-color 0.3s;

    &:hover:not(.lk-date__day--active) {
      background-color: #F3F4F5;
    }

    &--active {
      color: var(--white);
      background-color: #8557E5;
      box-shadow: 0px 2px 6px rgba(42, 46, 59, 0.24);
    }
  }
}

.lk-date-calendar {
  --dp-border-radius: 8px;
  --dp-border-color: #E2E2E7;
  --dp-border-color-hover: #E2E2E7;
  --dp-input-padding: 14px 20px;
  --dp-font-size: 15px;
  --dp-font-family: 'Inter';
  // --dp-input-icon-padding: 44px;

  width: 240px;

  ::v-deep .lk-date-calendar {
    &__input {
      height: 46px;
      font-weight: 500;
      transition: background-color 0.3s;

      &:hover {
        background-color: #F3F4F5;
      }
    }
  }
}
</style>
