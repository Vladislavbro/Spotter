<template>
  <div class="textarea">
    <textarea
      :value="value"
      :cols="cols"
      :rows="rows"
      :placeholder="placeholder"
      class="textarea__area"
      :disabled="disable"
      :maxlength="maxLength"
      :spellcheck="spellcheck"
      @input="$emit('update:modelValue', emitArgumentValue($event.target.value))"
    />
  </div>
</template>

<script>
export default {
  name: 'UIBaseTextarea',
  props: {
    modelValue: {
      type: undefined,
      required: false,
      default: '',
    },
    cols: {
      type: Number || String,
      required: false,
      default: 30,
    },
    rows: {
      type: Number || String,
      required: false,
      default: 7,
    },
    placeholder: {
      type: String,
      default: '',
    },
    maxLength: {
      type: Number || String,
      required: false,
      default: 1500,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    disable: {
      type: Boolean,
      required: false,
      default: false,
    },
    spellcheck: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  emits: ['update:modelValue', 'input'],
  computed: {
    value: {
      get () {
        return this.modelValue
      },
      set (value) {
        this.$emit('update:modelValue', value)
      },
    },
  },
  methods: {
    emitArgumentValue (value) {
      if (!value) {
        return ''
      }
      return value
    },
  },
}
</script>

<style lang="scss" scoped>
.textarea {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;

  &__area {
    position: relative;
    width: 100%;
    font-size: 14px;
    line-height: 21px;
    letter-spacing: -0.1px;
    min-height: 50px;
    padding: 16px;
    border: 1px solid var(--gray);
    border-radius: 8px;
    resize: none;
    outline: none;

    &::placeholder {
      color: var(--grayDark);
    }
  }
}
</style>
