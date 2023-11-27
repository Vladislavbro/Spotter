<template>
  <div class="filter-lk">
    <label class="filter-lk__label">
      {{ label }}
    </label>

    <div class="filter-lk__box">
      <div
        ref="inputsRef"
        class="filter-lk__inputs"
      >
        <div class="filter-lk__input">
          <span class="filter-lk__prefix">
            от
          </span>
          <input
            type="number"
            :value="from"
            :placeholder="minValue.toLocaleString()"
            :min="minValue"
            :max="maxValue - 1"
            autocomplete="off"
            class="filter-lk__input-area"
            @keypress="onKeypress($event)"
            @input="onInput($event, 'from')"
          >
        </div>
        <div class="filter-lk__input">
          <span class="filter-lk__prefix">
            до
          </span>
          <input
            type="number"
            :value="to"
            :placeholder="maxValue.toLocaleString()"
            :min="minValue + 1"
            :max="maxValue"
            autocomplete="off"
            class="filter-lk__input-area filter-lk__input-area--to"
            @keypress="onKeypress($event)"
            @input="onInput($event, 'to')"
          >
        </div>
        <div
          v-if="doubleType"
          class="filter-lk__types"
        >
          <button
            :class="['filter-lk__type', { 'filter-lk__type--active' : type === 'number'}]"
            @click.prevent="type = 'number'"
          >
            шт
          </button>
          <button
            :class="['filter-lk__type', { 'filter-lk__type--active' : type === 'percent'}]"
            @click.prevent="type = 'percent'"
          >
            %
          </button>
        </div>
      </div>

      <div
        ref="sliderRef"
        class="filter-lk__slider"
      >
        <input
          :value="from || minValue"
          type="range"
          :min="minValue"
          :max="maxValue - 1"
          autocomplete="off"
          @input="$emit('update:from', parseInt($event.target.value) || 0)"
        >
        <input
          :value="to || maxValue"
          type="range"
          :min="minValue + 1"
          :max="maxValue"
          autocomplete="off"
          @input="$emit('update:to', parseInt($event.target.value) || 0)"
        >

        <div class="filter-lk__track-wrapper">
          <div class="filter-lk__track" />
          <div class="filter-lk__range-between" />
          <div class="filter-lk__thumb filter-lk__thumb--left" />
          <div class="filter-lk__thumb filter-lk__thumb--right" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  from: {
    type: undefined,
    default: null,
  },
  to: {
    type: undefined,
    default: null,
  },
  label: {
    type: String,
    default: '',
  },
  doubleType: {
    type: Boolean,
    default: false,
  },
  minValue: {
    type: Number,
    default: 0,
  },
  maxValue: {
    type: Number,
    default: 1,
  },
})

const emits = defineEmits(['update:from', 'update:to'])

const type = ref('number')
const inputsRef = ref(null)
const sliderRef = ref(null)

watch(() => props.from, () => {
  nextTick(() => {
    createslider(false)
  })
})

watch(() => props.to, () => {
  nextTick(() => {
    createslider(false)
  })
})

const createslider = (firstPaint) => {
  const sliderValue = sliderRef.value
  const sliders = sliderValue.querySelectorAll('input')

  const thumbLeft = sliderValue.querySelector('.filter-lk__thumb--left')
  const thumbRight = sliderValue.querySelector('.filter-lk__thumb--right')
  const rangeBetween = sliderValue.querySelector('.filter-lk__range-between')

  const [sliderStart, sliderEnd] = sliders

  setStartValueCustomSlider(sliderStart, sliderEnd, thumbLeft, rangeBetween)
  setEndValueCustomSlider(sliderEnd, sliderStart, thumbRight, rangeBetween)

  if (firstPaint) {
    setEvents(sliderStart, sliderEnd, thumbLeft, thumbRight, rangeBetween)
  }
}

const setStartValueCustomSlider = (sliderStart, sliderEnd, pseudoEl, range) => {
  const maximum = Math.min(parseInt(sliderStart.value), parseInt(sliderEnd.value) - 1)
  const percent = ((maximum - sliderStart.min) / (sliderStart.max - sliderStart.min)) * 100

  const left = percent + '%'

  pseudoEl.style.left = left
  range.style.left = left
}

const setEndValueCustomSlider = (sliderEnd, sliderStart, pseudoEl, range) => {
  const minimum = Math.max(parseInt(sliderEnd.value), parseInt(sliderStart.value) + 1)
  const percent = ((minimum - sliderEnd.min) / (sliderEnd.max - sliderEnd.min)) * 100

  const right = 100 - percent + '%'

  pseudoEl.style.right = right
  range.style.right = right
}

const setEvents = (
  sliderStart,
  sliderEnd,
  thumbLeft,
  thumbRight,
  rangeBetween,
) => {
  sliderStart.addEventListener('input', () => {
    setStartValueCustomSlider(sliderStart, sliderEnd, thumbLeft, rangeBetween)
  })

  sliderEnd.addEventListener('input', () => {
    setEndValueCustomSlider(sliderEnd, sliderStart, thumbRight, rangeBetween)
  })
}

const onKeypress = (e) => {
  const charCode = (e.which) ? e.which : e.keyCode
  if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
    e.preventDefault()
  } else {
    return true
  }
}

const onInput = (e, type) => {
  const value = parseInt(e.target.value)

  if (type === 'from') {
    if (!isNaN(value) && value > props.maxValue - 1) {
      emits('update:from', null)
      nextTick(() => {
        emits('update:from', props.maxValue - 1)
      })
    } else if (!isNaN(value) && value < props.minValue) {
      emits('update:from', null)
      nextTick(() => {
        emits('update:from', props.minValue)
      })
    } else {
      emits('update:from', value)
    }
  } else if (type === 'to') {
    if (!isNaN(value) && value > props.maxValue) {
      emits('update:to', null)
      nextTick(() => {
        emits('update:to', props.maxValue)
      })
    } else if (!isNaN(value) && value < props.minValue + 1) {
      emits('update:to', null)
      nextTick(() => {
        emits('update:to', props.minValue + 1)
      })
    } else {
      emits('update:to', value)
    }
  }
}

onMounted(() => {
  createslider(true)
})

onBeforeUnmount(() => {
  const sliderValue = sliderRef.value
  const sliders = sliderValue.querySelectorAll('input')

  const [sliderStart, sliderEnd] = sliders

  sliderStart.replaceWith(sliderStart.cloneNode(true))
  sliderEnd.replaceWith(sliderEnd.cloneNode(true))
})
</script>

<style lang="scss" scoped>
.filter-lk {
  display: flex;
  flex-direction: column;

  &__label {
    display: block;
    margin-bottom: 9px;
    font-weight: 500;
    font-size: 14px;
    line-height: 18px;
  }

  &__box {
    display: flex;
    flex-direction: column;
  }

  &__inputs {
    display: grid;
    grid-template-columns: repeat(3, auto);
    margin-bottom: 24px;
    border: 1px solid #E9E9EA;
    border-radius: 4px;
  }

  &__input {
    position: relative;

    &:first-child {
      border-right: 1px solid #E9E9EA;
    }
  }

  &__prefix {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    top: 0;
    bottom: 0;
    left: 0;
    padding-left: 12px;
    font-size: 14px;
    line-height: 18px;
    color: #8B8B91;
  }

  &__input-area {
    width: 100%;
    height: 42px;
    padding-left: 32px;
    background: var(--white);
    border: 0;
    outline: none;
    appearance: none;
    -moz-appearance: textfield;

    &--to {
      padding-left: 34px;
    }

    &::-webkit-input-placeholder {
      color: #8B8B91;
    }
    &:-moz-placeholder {
      color: #8B8B91;
      opacity: 1;
    }
    &::-moz-placeholder {
      color: #8B8B91;
      opacity: 1;
    }
    &:-ms-input-placeholder {
      color: #8B8B91;
    }
    &::-ms-input-placeholder {
      color: #8B8B91;
    }
    &::placeholder {
      color: #8B8B91;
    }

    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
    }
  }

  &__types {
    display: flex;
    align-items: center;
    margin-right: 4px;
  }

  &__type {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 34px;
    font-size: 14px;
    line-height: 18px;
    background: #e9eaec;

    &--active {
      color: var(--white);
      background: #8557E5;
    }

    &:first-child {
      border-radius: 4px 0 0 4px;
    }

    &:last-child {
      border-radius: 0 4px 4px 0;
    }
  }

  &__slider {
    position: relative;
    width: 100%;

    input[type='range'] {
      position: absolute;
      bottom: 0;
      width: 100%;
      height: 2px;
      opacity: 0;
      cursor: pointer;
      pointer-events: none;
      -webkit-appearance: none;
      z-index: 2;

      &::-webkit-slider-thumb {
        pointer-events: all;
        width: 24px;
        height: 24px;
        border-radius: 0;
        border: 0 none;
        -webkit-appearance: none;
      }

      &::-moz-range-thumb {
        pointer-events: all;
        width: 24px;
        height: 24px;
        border-radius: 0;
        border: 0 none;
        -webkit-appearance: none;
      }
    }
  }

  &__track-wrapper {
    position: relative;
    height: 2px;
    display: grid;
    align-items: center;
    margin: 0 calc(24px / 2);
    z-index: 1;
  }

  &__track {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: #d9d9e0;
    z-index: 1;
  }

  &__range-between {
    position: absolute;
    top: 0;
    right: 0%;
    bottom: 0;
    left: 0%;
    background: #8557e5;
    z-index: 2;
  }

  &__thumb {
    position: absolute;
    width: 24px;
    height: 24px;
    background: #F3F4F5;
    border-radius: 50%;
    z-index: 3;

    &:before {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      width: 8px;
      height: 8px;
      background: #8557E5;
      border-radius: 50%;
      transform: translate(-50%, -50%);
    }

    &--left {
      left: 0%;
      transform: translate(calc(24px / -2), 0px);
    }

    &--right {
      right: 0%;
      transform: translate(calc(24px / 2), 0px);
    }
  }
}
</style>
