<template>
  <label
    :for="id"
    :class="['input', { 'input--password' : type === 'password' }, { 'input--error' : !!error }]"
  >
    <span v-if="label" class="input__label">
      {{ label }}
    </span>

    <input
      v-if="type === 'tel'"
      :id="id"
      v-maska
      data-maska="+7 (###) ###-##-##"
      type="tel"
      :value="modelValue || value"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      autocomplete="off"
      class="input__area"
      @input="$emit('update:modelValue', $event.target.value)"
    >

    <input
      v-else
      :id="id"
      :value="modelValue || value"
      :placeholder="placeholder"
      :type="currentType"
      :disabled="disabled"
      :required="required"
      autocomplete="off"
      class="input__area"
      @input="$emit('update:modelValue', $event.target.value)"
    >

    <span
      v-if="type === 'password'"
      class="input__eye"
      @click="toggleEye()"
    >
      <UIBaseIcon v-show="isShowPassword" name="icon-eye" />
      <UIBaseIcon v-show="!isShowPassword" name="icon-eye-close" />
    </span>

    <span v-if="error" class="input__error">
      {{ error }}
    </span>
  </label>
</template>

<script setup>
import { vMaska } from 'maska'

const props = defineProps({
  id: {
    type: String,
    default: '',
  },
  value: {
    type: String,
    default: '',
  },
  modelValue: {
    type: undefined,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  label: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  required: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const isShowPassword = ref(false)

const currentType = computed(() => {
  if (props.type === 'password') {
    if (!isShowPassword.value) {
      return 'password'
    } else {
      return 'text'
    }
  }

  return props.type
})

const toggleEye = () => {
  isShowPassword.value = !isShowPassword.value
}
</script>

<style lang="scss" scoped>
.input {
  position: relative;
  display: block;
  width: 100%;
  font-feature-settings: 'pnum' on, 'lnum' on;

  &--error {
    .input {
      &__area {
        border: 1px solid var(--red);
      }
    }
  }

  &--password {
    .input {
      &__area {
        padding-right: 56px;
      }
    }
  }

  &__label {
    margin-bottom: 4px;
    font-weight: 500;
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-medium) {
      font-size: 14px;
    }
  }

  &__area {
    width: 100%;
    height: 44px;
    padding: 12px 16px;
    font-size: 14px;
    line-height: 20px;
    background: var(--white);
    border: 1px solid #E2E2E7;
    border-radius: 4px;
    outline: none;
    transition: all 0.3s;

    @include mq($bp-medium) {
      height: 54px;
      padding: 16px 20px;
      font-size: 15px;
      line-height: 22px;
    }

    &:hover {
      border: 1px solid #18181C;
    }

    &:focus {
      border: 3px solid #D9D9E0;
    }

    &:disabled {
      background: #F8F8F8;
      border: 0;
    }

    &::-webkit-input-placeholder {
      color: var(--gray);
    }
    &:-moz-placeholder {
      color: var(--gray);
      opacity:  1;
    }
    &::-moz-placeholder {
      color: var(--gray);
      opacity:  1;
    }
    &:-ms-input-placeholder {
      color: var(--gray);
    }
    &::-ms-input-placeholder {
      color: var(--gray);
    }
    &::placeholder {
      color: var(--gray);
    }
  }

  &__error {
    margin-top: 4px;
    color: var(--red);
    font-size: 12px;
    line-height: 14px;
  }

  &__eye {
    position: absolute;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    height: 54px;
    padding: 0 16px;
    cursor: pointer;
    z-index: 20;
  }
}
</style>
