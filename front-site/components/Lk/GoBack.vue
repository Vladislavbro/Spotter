<template>
  <NuxtLink
    :to="link"
    class="go-back"
  >
    <span class="go-back__icon">
      <UIBaseIcon name="lk/icon-arrow-left" />
    </span>
    {{ text }}
  </NuxtLink>
</template>

<script setup>
defineProps({
  link: {
    type: String,
    default: '',
  },
  text: {
    type: String,
    default: '',
  }
})
</script>

<style lang="scss" scoped>
.go-back {
  display: flex;
  align-items: center;
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    margin-right: 12px;
    background: var(--white);
    box-shadow: 0px 2px 6px rgba(44, 48, 64, 0.2);
    border-radius: 4px;
  }
}
</style>
