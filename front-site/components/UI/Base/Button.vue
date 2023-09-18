<template>
  <component
    :is="tag"
    class="button"
    :type="type"
    :to="to"
    :href="href"
    :class="{
      'button_black-outline': primaryBlackOutline,
      'button_white-outline': primaryWhiteOutline,
      'button_green': primaryGreen,
      'button_green-outline': primaryGreenOutline,
      'button_big': big,
      'button_full-width': fullWidth
    }"
    :disabled="disable"
  >
    <UIBaseLoader
      v-if="loading"
      class="button__loader"
    />
    <span
      v-else
      class="button__text"
    >
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
  primaryBlackOutline: {
    type: Boolean,
    default: false,
  },
  primaryWhiteOutline: {
    type: Boolean,
    default: false,
  },
  primaryGreen: {
    type: Boolean,
    default: false,
  },
  primaryGreenOutline: {
    type: Boolean,
    default: false,
  },
  big: {
    type: Boolean,
    default: false,
  },
  disable: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  fullWidth: {
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
.button {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 10px 24px;
  font-weight: 500;
  font-size: 13px;
  line-height: 16px;
  text-align: center;
  color: var(--white);
  background: var(--blackMain);
  border: 1px solid var(--blackLight);
  border-radius: 60px;
  transition: all 0.3s;

  @include mq($bp-medium) {
    padding: 16px 28px;
    font-size: 14px;
    line-height: 16px;
  }

  &:hover {
    background: var(--blackLight);
  }

  &_big {
    padding: 16px 24px;
    font-size: 14px;
    line-height: 16px;

    @include mq($bp-medium) {
      padding: 20px 40px;
      font-size: 16px;
      line-height: 22px;
    }
  }

  &_full-width {
    width: 100%;
  }

  &_black-outline {
    color: var(--blackMain);
    background: none;
    border-color: var(--blackMain);

    &:hover {
      color: var(--white);
      background: var(--blackMain);
    }
  }

  &_white-outline {
    color: var(--white);
    background: none;
    border-color: var(--white);

    &:hover {
      color: var(--blackMain);
      background: var(--white);
    }
  }

  &_green-outline {
    color: var(--lime);
    border-color: var(--lime);

    &:hover {
      color: var(--blackMain);
      background: var(--lime);
    }
  }

  &_green {
    color: var(--blackMain);
    background: var(--lime);
    border: 0;

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
