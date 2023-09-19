<template>
  <div :class="[`subscribe-card subscribe-card--${item.type}`, { 'subscribe-card--lk' : isLk }]">
    <div class="subscribe-card__body">
      <p class="subscribe-card__title">
        {{ item.title }}

        <span v-if="item.type === 'premium'" class="subscribe-card__status">
          + 5 дней бесплатно
        </span>
      </p>

      <p class="subscribe-card__text">
        {{ item.text }}
      </p>

      <p class="subscribe-card__price">
        {{ item.price }}
        <small v-if="item.type !== 'trial'">
          / за месяц
        </small>
      </p>

      <UIBaseButton
        :text="item.textBtn"
        :primary-green="item.type === 'premium'"
        class="subscribe-card__btn"
        @click.prevent="emits('subscribe', item.type)"
      />
    </div>

    <div class="subscribe-card__footer">
      <ul class="subscribe-card__list">
        <li
          v-for="(text, t) in item.list"
          :key="t"
          class="subscribe-card__item"
        >
          {{ text }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  isLk: {
    type: Boolean,
    default: false,
  },
})

const emits = defineEmits(['subscribe'])
</script>

<style lang="scss" scoped>
.subscribe-card {
  display: flex;
  flex-direction: column;
  color: var(--blackMain);
  background: #F3F4F5;
  border: 1px solid #DFDFE3;
  border-radius: 32px;

  &--lk {
    background: var(--white);
    border-radius: 24px;

    .subscribe-card {
      &__body {
        padding: 28px 28px 20px;
      }

      &__footer {
        padding: 20px 28px 40px;
      }
    }
  }

  &--premium {
    color: var(--white);
    background: var(--blackMain);
    border-color: #393940;

    .subscribe-card {
      &__body {
        border-color: #393940;
      }

      &__text {
        color: var(--grayLight);
      }
    }
  }

  &__body {
    display: flex;
    flex-direction: column;
    padding: 20px 24px;
    border-bottom: 1px solid #DFDFE3;

    @include mq($bp-small) {
      padding: 32px;
    }
  }

  &__title {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-weight: 500;
    font-size: 18px;
    line-height: 24px;

    @include mq($bp-small) {
      font-size: 24px;
      line-height: 30px;
    }
  }

  &__status {
    margin-left: 8px;
    padding: 4px;
    color: var(--blackMain);
    font-weight: 500;
    font-size: 10px;
    line-height: 12px;
    background: var(--lime);
    border-radius: 4px;

    @include mq($bp-small) {
      margin-left: 12px;
      padding: 4px 8px;
      font-size: 12px;
      line-height: 14px;
    }
  }

  &__text {
    margin-bottom: 8px;
    color: var(--grayBlack);
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small) {
      margin-bottom: 16px;
      font-size: 15px;
      line-height: 22px;
    }
  }

  &__price {
    display: flex;
    align-items: flex-end;
    margin-bottom: 12px;
    font-weight: 500;
    font-size: 28px;
    line-height: 32px;

    @include mq($bp-small) {
      margin-bottom: 24px;
      font-size: 36px;
      line-height: 40px;
    }

    small {
      margin-left: 4px;
      font-weight: 400;
      font-size: 13px;
      line-height: 18px;

      @include mq($bp-small) {
        font-size: 15px;
        line-height: 22px;
      }
    }
  }

  &__footer {
    padding: 16px 24px 28px;

    @include mq($bp-small) {
      padding: 20px 32px 40px;
    }
  }

  &__list {
    display: grid;
    grid-gap: 8px;

    @include mq($bp-small) {
      grid-gap: 12px;
    }
  }

  &__item {
    display: flex;
    align-items: flex-start;
    font-size: 14px;
    line-height: 20px;

    @include mq($bp-small) {
      font-size: 15px;
      line-height: 22px;
    }

    &:before {
      content: '';
      flex: 0 0 auto;
      display: block;
      width: 20px;
      height: 20px;
      margin-right: 8px;
      background: var(--lime) url('@/assets/icons/landing/icon-galka.svg')no-repeat 50%;
      background-size: 8px;
      border-radius: 50%;

      @include mq($bp-small) {
        width: 28px;
        height: 28px;
        margin-right: 12px;
        background-size: auto;
      }
    }
  }
}
</style>
