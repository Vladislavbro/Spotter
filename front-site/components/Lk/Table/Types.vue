<template>
  <div class="table-types">
    <button
      :class="['table-types__btn', { 'table-types__btn--active' : value === 'fbo' }]"
      @click.prevent="emits('change', 'fbo')"
    >
      FBO
      <LkTooltip
        text="Продажи со склада маркетплейса"
        direction="bottom"
        icon="question"
      />
    </button>

    <button
      :class="['table-types__btn', { 'table-types__btn--active' : value === 'fbs' }]"
      @click.prevent="emits('change', 'fbs')"
    >
      FBS
      <LkTooltip
        text="Продажи со склада поставщика"
        direction="bottom"
        icon="question"
      />
    </button>
  </div>
</template>

<script setup>
defineProps({
  value: {
    type: String,
    default: 'fbo',
  },
})

const emits = defineEmits(['change'])
</script>

<style lang="scss" scoped>
.table-types {
  display: flex;
  align-items: center;

  &__btn {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: center;
    height: 46px;
    padding: 0px 24px;
    font-weight: 500;
    font-size: 15px;
    line-height: 18px;
    background: var(--white);
    border: 1px solid #E2E2E7;

    &--active {
      color: var(--white);
      background: #8557E5;

      ::v-deep(.ui-icon) {
        path {
          fill: var(--white);
        }
      }
    }

    &:first-child {
      border-radius: 8px 0 0 8px;
    }

    &:last-child {
      border-radius: 0 8px 8px 0;
    }
  }
}
</style>
