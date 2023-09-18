<template>
  <div class="reviews-card">
    <div class="reviews-card__header">
      <div class="reviews-card__user">
        <div class="reviews-card__user-avatar">
          <img :src="item.image" alt="">
        </div>
        <div class="reviews-card__user-content">
          <p class="reviews-card__user-name">
            {{ item.name }}
          </p>
          <p class="reviews-card__date">
            {{ item.date }}
          </p>
        </div>
      </div>

      <div class="reviews-card__rating">
        <UIBaseIcon
          v-for="i in 5"
          :key="i"
          name="landing/icon-star"
        />
      </div>
    </div>

    <div class="reviews-card__body">
      <p
        ref="commentRef"
        :class="['reviews-card__comment', { 'reviews-card__comment--hide' : isHide }]"
      >
        {{ item.text }}
      </p>
      <a
        v-if="isHide"
        href="#"
        rel="nofollow"
        class="reviews-card__more"
        @click.prevent="isHide = false"
      >
        еще
      </a>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})

const commentRef = ref(null)
const isHide = ref(false)

const checkComment = () => {
  const height = commentRef.value.offsetHeight
  if (height > 288) {
    isHide.value = true
  }
}

onMounted(() => {
  checkComment()
})
</script>

<style lang="scss" scoped>
.reviews-card {
  display: grid;
  grid-gap: 8px;

  padding: 16px;

  background: var(--white);
  border: 1px solid #E9E9EA;
  border-radius: 20px;

  @include mq($bp-small) {
    grid-gap: 16px;

    padding: 28px 28px 34px 28px;
  }

  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-direction: column;
    grid-gap: 12px;

    @include mq($bp-small) {
      flex-direction: row;
    }
  }

  &__user {
    display: grid;
    grid-gap: 12px;
    grid-auto-flow: column;
    align-items: flex-start;
    justify-content: flex-start;

    @include mq($bp-small-medium) {
      grid-gap: 16px;
    }
  }

  &__user-avatar {
    width: 56px;
    height: 56px;

    border-radius: 50%;
    overflow: hidden;

    @include mq($bp-small-medium) {
      width: 64px;
      height: 64px;
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__user-content {
    display: grid;
    grid-gap: 2px;
  }

  &__user-name {
    font-weight: 600;
    font-size: 15px;
    line-height: 20px;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    @include mq($bp-small-medium) {
      font-size: 18px;
      line-height: 26px;
    }
  }

  &__date {
    color: var(--grayLight);
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small-medium) {
      font-size: 15px;
      line-height: 22px;
    }
  }

  &__rating {
    display: flex;
    align-self: start;
  }

  &__body {
    display: grid;
    grid-gap: 8px;
  }

  &__comment {
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small-medium) {
      font-size: 16px;
      line-height: 24px;
    }

    &--hide {
      max-height: 288px;
      overflow: hidden;
    }
  }

  &__more {
    color: var(--grayLight);
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small-medium) {
      font-size: 15px;
      line-height: 22px;
    }
  }
}
</style>
