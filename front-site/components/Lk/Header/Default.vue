<template>
  <header class="header">
    <div class="header__box">
      <div class="header__side">
        <CommonLogo class="header__logo" is-black />

        <LkHeaderSearch
          v-if="!route.fullPath.includes('/search')"
          class="header__search"
        />
      </div>

      <div class="header__side header__side--end">
        <LkHeaderTarif class="header__tarif" />

        <UILkButton
          to="/lk/profile"
          text="Личный кабинет"
          primary-gray-outline
          class="header__link"
        />
      </div>
    </div>
  </header>
</template>

<script setup>
const route = useRoute()
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  color: var(--white);
  background: var(--white);
  z-index: 100;

  &__box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 54px 12px 32px;
  }

  &__side {
    flex: 1 1 auto;
    display: flex;
    align-items: center;

    &--end {
      justify-content: flex-end;
    }
  }

  &__logo {
    margin-right: 28px;
  }

  &__search {
    width: 100%;
    max-width: 600px;
  }

  &__link {
    margin-left: 16px;
  }
}
</style>
