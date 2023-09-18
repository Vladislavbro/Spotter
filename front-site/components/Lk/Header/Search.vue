<template>
  <NuxtLink
    to="/lk/search"
    class="header-search"
  >
    <div class="header-search__box">
      <span class="header-search__loop">
        <UIBaseIcon name="lk/icon-loop" />
      </span>

      <UIBaseInput
        placeholder="Поиск по товару, бренду, продавцу и нише"
        class="header-search__input"
      />
    </div>
  </NuxtLink>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.header-search {
  position: relative;
  color: var(--blackMain);
  cursor: pointer;

  &__box {
    position: relative;
    z-index: 101;
  }

  &__loop {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 20px;
    display: flex;
    align-items: center;
    z-index: 1;

    ::v-deep(.ui-icon) {
      svg {
        width: 16px;
        height: 16px;

        & > * {
          fill: var(--grayLight);
        }
      }
    }
  }

  &__input {
    ::v-deep(.input__area) {
      height: 48px;
      padding: 15px 44px;
      line-height: 18px;
      border-radius: 8px;
    }
  }
}
</style>
