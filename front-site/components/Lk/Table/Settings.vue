<template>
  <div
    v-click-outside="close"
    class="lk-settings"
  >
    <button
      class="lk-settings__btn"
      @click.prevent="isOpen = !isOpen"
    >
      <UIBaseIcon
        name="lk/icon-settings"
        class="lk-settings__icon"
      />

      Настройка таблицы
    </button>

    <div
      v-if="isOpen"
      :class="['lk-settings__dropdown', { 'lk-settings-dropdown--active' : isOpen }]"
    >
      <div class="lk-settings__list">
        <div
          v-for="(item, i) in array"
          :key="i"
          class="lk-settings__item"
        >
          <UILkCheckbox
            v-model="item.show"
            :text="item.label"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  array: {
    type: Array,
    default: () => ([]),
  },
})

const isOpen = ref(false)

const close = () => {
  isOpen.value = false
}
</script>

<style lang="scss" scoped>
.lk-settings {
  position: relative;

  &__btn {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    height: 44px;
    padding: 0 20px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    background: #F3F4F5;
    border: 1px solid #F3F4F5;
    border-radius: 8px;

    &:hover {
      border-color: #E2E2E7;
    }
  }

  &__dropdown {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    width: 300px;
    background: var(--white);
    border: 1px solid #E2E2E7;
    box-shadow: 0px 4px 20px rgba(44, 48, 64, 0.12);
    border-radius: 8px;
    z-index: 100;
  }

  &__list {
    display: flex;
    flex-direction: column;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
  }

  &__item {
    padding: 16px 20px;
    border-top: 1px solid #E9E9EA;

    &:first-child {
      border-top: 0;
    }
  }
}
</style>
