<template>
  <label
    :for="id"
    class="radio-lk"
  >
    <input
      :id="id"
      :value="value"
      :checked="isChecked"
      type="radio"
      class="radio-lk__input"
      @change="$emit('update:modelValue', $event.target.value)"
    >

    <span
      class="radio-lk__icon"
    />

    <span
      v-if="text"
      class="radio-lk__text"
    >
      {{ text }}
    </span>
  </label>
</template>

<script setup>
const props = defineProps({
  id: {
    type: String,
    default: '',
  },
  modelValue: {
    type: undefined,
    default: '',
  },
  value: {
    type: undefined,
    default: '',
  },
  text: {
    type: String,
    default: '',
  },
})

const isChecked = computed(() => {
  return props.modelValue === props.value
})
</script>

<style lang="scss" scoped>
.radio-lk {
  display: flex;
  align-items: center;
  cursor: pointer;

  &:hover {
    .radio-lk {
      &__icon {
        border-color: #8557E5;
      }

      &__text {
        color: #8557E5;
      }
    }
  }

  &__input {
    display: none;

    &:checked {
      & + .radio-lk__icon {
        border: 6px solid #8557e5;
      }
    }
  }

  &__icon {
    width: 20px;
    height: 20px;
    background: var(--white);
    border: 1px solid #D9D9E0;
    border-radius: 50%;
  }

  &__text {
    margin-left: 8px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
  }
}
</style>
