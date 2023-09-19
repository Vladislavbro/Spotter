<template>
  <component
    :is="tag"
    class="button-lk"
    :type="type"
    :to="to"
    :href="href"
    :class="{
      'button-lk--gray': primaryGray,
      'button-lk--gray-outline': primaryGrayOutline,
      'button-lk--green': primaryGreen,
      'button-lk--full-width': fullWidth,
      'button-lk--big': isBig
    }"
    :disabled="disable"
  >
    <span class="button-lk__text">
      {{ text }}
    </span>
  </component>
</template>

<script setup>
import { NuxtLink } from '#components'

const props = defineProps({
  text: {
    type: String,
    default: '',
  },
  to: {
    type: String,
    default: '',
  },
  href: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'button',
  },
  primaryGray: {
    type: Boolean,
    default: false,
  },
  primaryGrayOutline: {
    type: Boolean,
    default: false,
  },
  primaryGreen: {
    type: Boolean,
    default: false,
  },
  disable: {
    type: Boolean,
    default: false,
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
  isBig: {
    type: Boolean,
    default: false,
  },
})

const tag = computed(() => {
  if (props.to) {
    return NuxtLink
  } else if (props.href) {
    return 'a'
  } else {
    return 'button'
  }
})
</script>

<style lang="scss">
.button-lk {
  position: relative;
  padding: 10px 18px;
  font-weight: 500;
  font-size: 13px;
  line-height: 16px;
  text-align: center;
  color: var(--white);
  background: var(--blackMain);
  border: 1px solid var(--blackLight);
  border-radius: 60px;
  transition: all 0.3s;

  &:hover {
    background: var(--blackLight);
  }

  &--full-width {
    width: 100%;
  }

  &--big {
    padding: 19px;
    font-size: 14px;
  }

  &--gray {
    color: var(--blackMain);
    background: #F2F2F4;
    border-color: #F2F2F4;

    &:hover {
      background: #F2F2F4;
    }
  }

  &--gray-outline {
    color: var(--blackMain);
    background: var(--white);
    border-color: #E9E9EA;

    &:hover {
      border-color: var(--blackMain);
      background: var(--white);
    }
  }

  &--green {
    color: var(--blackMain);
    background: var(--lime);
    border-color: var(--lime);

    &:hover {
      background: var(--limeLight);
    }
  }

  &__text {
    position: relative;
    z-index: 2;
  }

  // &:disabled {
  // }
}
</style>
