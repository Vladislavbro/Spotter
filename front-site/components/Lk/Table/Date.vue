<template>
  <div :class="['lk-date', { 'lk-date--calendar': calendarOnly }]">
    <!-- <VueDatePicker
      v-model="date"
      range
      format="dd.MM.yyyy"
      model-type="yyyy-MM-dd"
      :auto-range="day"
      multi-calendars="3"
      :month-change-on-scroll="false"
      month-name-format="long"
      :clearable="false"
      :enable-time-picker="false"
      locale="ru"
      input-class-name="lk-date-calendar__input"
      class="lk-date-calendar"
      @update:model-value="emitChange"
    >
      <template #action-row="{ closePicker, selectDate }">
        <div class="dp__action_buttons">
          <button class="dp__action_button dp__action_cancel" @click="setDefaultDate(), closePicker()">
            Сбросить
          </button>
          <button class="dp__action_button dp__action_select" @click="selectDate">
            Применить
          </button>
        </div>
      </template>
    </VueDatePicker> -->

    <div
      v-if="!calendarOnly"
      class="lk-date__days"
    >
      <button
        v-for="(item, i) in days"
        :key="i"
        :class="['lk-date__day', { 'lk-date__day--active' : day === item.value }]"
        @click.prevent="setDay(item.value)"
      >
        {{ item.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
// import VueDatePicker from '@vuepic/vue-datepicker'
// import '@vuepic/vue-datepicker/dist/main.css'
// import { format, sub } from 'date-fns'

defineProps({
  calendarOnly: {
    type: Boolean,
    default: false,
  },
})

const emits = defineEmits(['change'])

const days = [
  { label: '7 дней', value: 7 },
  { label: '14 дней', value: 14 },
  { label: 'месяц', value: 30 },
]

const day = ref(30)
// const date = ref([
//   format(sub(new Date(), { days: day.value }), 'yyyy-MM-dd'),
//   format(new Date(), 'yyyy-MM-dd'),
// ])
const date = null

const setDay = (data) => {
  day.value = data
  setDefaultDate()
}

const setDefaultDate = () => {
  // date.value = [
  //   format(sub(new Date(), { days: day.value }), 'yyyy-MM-dd'),
  //   format(new Date(), 'yyyy-MM-dd'),
  // ]

  emitChange()
}

const emitChange = () => {
  emits('change', {
    day: day.value,
    // date: date.value[1],
    date,
  })
}
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
  --dp-font-size: 12px;
  --dp-font-family: 'Inter';
  --dp-menu-padding: 20px 28px 0 28px;
  --dp-action-row-padding: 24px 28px 20px;
  --dp-cell-size: 30px;
  --dp-row-maring: 0;
  --dp-month-year-row-button-size: 24px;
  --dp-button-icon-height: 12px;
  // --dp-input-icon-padding: 44px;

  width: 240px;

  ::v-deep {
    .dp__theme_light {
      --dp-primary-color: #8557E5;
      --dp-hover-color: #F3EAFF;
      --dp-icon-color: black;
    }

    .lk-date-calendar {
      &__input {
        height: 46px;

        line-height: 18px;
        font-size: 15px;
        font-weight: 500;
        transition: background-color 0.3s;

        &:hover {
          background-color: #F3F4F5;
        }
      }
    }

    .dp--arrow-btn-nav {
      background: #F1F0F1;
      border-radius: 4px;
    }

    .dp__arrow_top,
    .dp__calendar_header_separator {
      display: none;
    }

    .dp__menu_inner {
      grid-gap: 14px;
    }

    .dp__calendar_header_item {
      color: var(--grayLight);
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }

    .dp__action_row {
      justify-content: center;
    }

    .dp__action_buttons {
      grid-gap: 8px;
      margin-inline-start: unset;
    }

    .dp__action_button {
      height: 30px;
      padding: 8px 16px;
      margin-inline-start: unset;
      border-radius: 60px;
    }

    .dp__action_cancel {
      background: #F3F4F5;
      border: 0;
    }

    .dp__action_select {
      background: var(--blackMain);
    }
  }
}
</style>
