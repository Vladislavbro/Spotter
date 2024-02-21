<template>
  <div class="body">
    <LandingHeaderDefault />

    <slot />

    <LandingFooterDefault />
  </div>
</template>

<script setup>
</script>

<style scoped lang="scss">
.body {
  padding-top: 61px;

  @include mq($bp-medium) {
    padding-top: 71px;
  }
}
</style>
