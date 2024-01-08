<template>
  <div class="layout-lk">
    <LkHeaderDefault />

    <LkAsideDefault />

    <div class="layout-lk__box">
      <slot />

      <LandingFooterDefault
        theme-light
        layout="lk"
      />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped lang="scss">
.layout-lk {
  display: flex;
  min-height: 100vh;
  padding: 72px 0 0 120px;
  font-family: 'Inter';
  color: var(--blackMain);
  background: #F3F4F5;

  &__box {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
  }
}
</style>
