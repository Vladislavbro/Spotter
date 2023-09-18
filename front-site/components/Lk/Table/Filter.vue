<template>
  <div class="lk-filter">
    <div class="lk-filter__header">
      <UIBaseIcon name="lk/icon-filter" />
      Фильтры
    </div>

    <div :class="['lk-filter__box', { 'lk-filter__box--open' : isOpen }]">
      <slot />
    </div>

    <div class="lk-filter__footer">
      <div />

      <a
        href="#"
        :class="['lk-filter__show', { 'lk-filter__show--open' : isOpen }]"
        @click.prevent="toggle()"
      >
        {{ isOpen ? 'Свернуть параметры' : 'Показать все параметры' }}
        <UIBaseIcon
          name="lk/icon-arrow-down"
          class="lk-filter__icon"
        />
      </a>

      <div class="lk-filter__actions">
        <UILkButton
          text="Сбросить"
          primary-gray
          class="lk-filter__action"
          @click.prevent="emits('reset')"
        />

        <UILkButton
          text="Показать"
          class="lk-filter__action"
          @click.prevent="emits('submit')"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const emits = defineEmits(['submit', 'reset'])

const isOpen = ref(false)

const toggle = () => {
  isOpen.value = !isOpen.value
}
</script>

<style lang="scss" scoped>
.lk-filter {
  display: flex;
  flex-direction: column;
  padding: 20px 24px 16px 20px;
  background: var(--white);
  border-radius: 12px;

  &__header {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 21px;
    font-weight: 600;
    font-size: 16px;
    line-height: 20px;
  }

  &__box {
    display: grid;
    grid-gap: 33px;
    grid-template-columns: repeat(3, 1fr);
    max-height: 117px;
    padding-bottom: 12px;
    overflow: hidden;
    transition: max-height 0.3s;

    &--open {
      max-height: 1000px;
    }
  }

  &__footer {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    margin-top: 20px;
  }

  &__show {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: center;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    color: #8557E5;

    &--open {
      .lk-filter__icon {
        transform: rotate(180deg);
      }
    }
  }

  &__icon {
    transition: transform 0.3s;
  }

  &__actions {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;
    justify-content: flex-end;
  }

  &__action {
    font-size: 14px;
    border-radius: 8px;
  }
}
</style>
