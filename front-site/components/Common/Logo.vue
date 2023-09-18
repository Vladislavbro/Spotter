<template>
  <NuxtLink
    to="/"
    :class="['logo', { 'logo--black' : isBlack }]"
  >
    <UIBaseIcon name="icon-logo" filled />
  </NuxtLink>
</template>

<script setup>
defineProps({
  isBlack: {
    type: Boolean,
    default: false,
  },
})
</script>

<style lang="scss" scoped>
.logo {
  ::v-deep(.ui-icon) {
    svg {
      height: 36px;
    }
  }

  @include mq($bp-medium) {
    ::v-deep(.ui-icon) {
      svg {
        height: auto;
      }
    }
  }

  &--black {
    ::v-deep(.ui-icon) {
      .icon-logo__letter {
        fill: var(--black);
      }
    }
  }
}
</style>
