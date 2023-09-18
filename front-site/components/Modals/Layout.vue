<template>
  <div class="modal">
    <div class="modal__overlay" />

    <div class="modal__box" @click.self="onClickOverlay()">
      <div class="modal__wrap" @click.self="onClickOverlay()">
        <div class="modal__content" @click.self="onClickOverlay()">
          <a
            href="#"
            class="modal__close"
            @click.prevent="onClickOverlay()"
          >
            <UIBaseIcon name="icon-close" />
          </a>
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const emits = defineEmits(['close'])

const onClickOverlay = () => {
  emits('close')
}
</script>

<style lang="scss" scoped>
.modal {
  &__overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
  }

  &__box {
    position: fixed;
    overflow-y: auto;
    overflow-x: hidden;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    text-align: center;
    white-space: nowrap;
    z-index: 2001;
  }

  &__wrap {
    position: relative;
    height: 100%;

    &:after {
      display: inline-block;
      vertical-align: middle;
      width: 0;
      height: 100%;
      content: '';
    }
  }

  &__content {
    display: inline-block;
    vertical-align: middle;
    position: relative;
    white-space: normal;
    text-align: left;
    margin: 20px auto;
  }

  &__close {
    position: absolute;
    top: 4px;
    right: 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    background: #F3F4F5;
    border-radius: 50%;

    @include mq($bp-small) {
      top: 12px;
      right: 12px;
      width: 48px;
      height: 48px;
    }
  }
}
</style>
