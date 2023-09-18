<template>
  <div class="top-items">
    <p class="top-items__title">
      ТОП-5 товаров ниши
    </p>

    <div class="top-items__cards">
      <LkNicheResumeTopItemsCard
        v-for="i in 5"
        :key="i"
      />
    </div>

    <UILkButton
      text="Смотреть все товары"
      class="top-items__btn"
    />
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.top-items {
  display: flex;
  flex-direction: column;

  &__title {
    margin-bottom: 28px;
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
  }

  &__cards {
    display: grid;
    grid-gap: 16px;
    grid-template-columns: repeat(5, 1fr);
    margin-bottom: 32px;
  }

  &__btn {
    height: 48px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    color: var(--blackMain);
    background: none;
    border-color: #D9D9E0;

    &:hover {
      background: none;
    }
  }
}
</style>
