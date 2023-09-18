<template>
  <div
    :class="[
      'lk-tooltip',
      `lk-tooltip--${direction}`,
      { 'lk-tooltip--white' : isWhite }
    ]"
  >
    <UIBaseIcon
      :name="getIconName"
      class="lk-tooltip__icon"
    />

    <div
      class="lk-tooltip__box"
    >
      {{ text }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  text: {
    type: String,
    default: '',
  },
  isWhite: {
    type: Boolean,
    default: false,
  },
  direction: {
    type: String,
    default: 'top',
  },
  icon: {
    type: String,
    default: 'info',
  },
})

const getIconName = computed(() => {
  switch (props.icon) {
    case 'info':
      return 'lk/icon-info'
    case 'question':
      return 'lk/icon-question'
    default:
      return ''
  }
})
</script>

<style lang="scss" scoped>
.lk-tooltip {
  position: relative;
  cursor: pointer;

  &--white {
    .lk-tooltip__box {
      color: var(--blackMain);
      background: var(--white);
    }
  }

  &--top {
    .lk-tooltip__box {
      bottom: calc(100% + 5px);
    }
  }

  &--bottom {
    .lk-tooltip__box {
      top: calc(100% + 5px);
    }
  }

  &__icon {
    &:hover {
      & + .lk-tooltip__box {
        display: block;
      }
    }
  }

  &__box {
    display: none;
    position: absolute;
    left: 50%;
    width: 230px;
    padding: 12px 16px;
    font-weight: 400;
    font-size: 12px;
    line-height: 14px;
    color: var(--white);
    background: var(--blackMain);
    box-shadow: 0px 2px 8px rgba(44, 48, 64, 0.2);
    border-radius: 8px;
    transform: translateX(-50%);
    z-index: 100;
  }
}
</style>
