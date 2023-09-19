<template>
  <label
    class="checkbox-lk"
  >
    <input
      :value="modelValue"
      :checked="modelValue"
      type="checkbox"
      @change="$emit('update:modelValue', $event.target.checked)"
    >
    <span
      class="checkbox-lk__icon"
    />

    <span
      v-if="text"
      class="checkbox-lk__text"
    >
      {{ text }}
    </span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: {
    type: undefined,
    default: false,
  },
  text: {
    type: String,
    default: '',
  },
})
</script>

<style lang="scss" scoped>
.checkbox-lk {
  display: flex;
  align-items: center;
  cursor: pointer;

  &:hover {
    .checkbox-lk {
      &__icon {
        border-color: #8557E5;
      }

      &__text {
        color: #8557E5;
      }
    }
  }

  input {
    display: none;

    &:checked {
      & + .checkbox-lk {
        &__icon {
          border-color: #8557E5;
          background: #8557E5 url(~/assets/icons/lk/icon-check.svg)no-repeat 50%;
        }
      }
    }
  }

  &__icon {
    width: 20px;
    height: 20px;
    background: var(--white);
    border: 1px solid #D9D9E0;
  }

  &__text {
    margin-left: 8px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
  }
}
</style>
