<template>
  <div class="perspective-card">
    <div class="perspective-card__content">
      <div class="perspective-card__header">
        <p class="perspective-card__title">
          {{ item.title }}
        </p>

        <div class="perspective-card__icon">
          <UIBaseIcon name="lk/icon-flag" />
        </div>
      </div>

      <p class="perspective-card__text">
        {{ item.text }}
      </p>
    </div>

    <p class="perspective-card__type">
      {{ item.type }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})
</script>

<style lang="scss" scoped>
.perspective-card {
  width: 100%;
  min-height: 250px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 20px 16px 16px;
  background: var(--white);
  border: 1px solid #E2E2E7;
  border-radius: 8px;

  &__content {
    display: flex;
    flex-direction: column;
  }

  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 8px;
  }

  &__title {
    margin-right: 8px;
    font-weight: 600;
    font-size: 16px;
    line-height: 20px;
  }

  &__icon {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: #E1F2EC;
    border-radius: 50%;
  }

  &__text {
    font-size: 13px;
    line-height: 18px;
    color: #7D7D91;
  }

  &__type {
    margin-top: 20px;
    padding: 4px 8px;
    font-weight: 500;
    font-size: 12px;
    line-height: 16px;
    color: #8557E5;
    background: #F3EAFF;
    border-radius: 60px;
  }
}
</style>
