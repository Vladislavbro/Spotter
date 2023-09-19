<template>
  <span
    class="ui-icon"
    :class="{ 'ui-icon--fill': filled }"
    v-html="icon"
  />
</template>

<script setup>
const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  filled: {
    type: Boolean,
    default: false,
  },
})

const icon = ref('')

watchEffect(async () => {
  try {
    const iconsImport = import.meta.glob('assets/icons/**/**.svg', {
      as: 'raw',
      eager: false,
    })
    const rawIcon = await iconsImport[`/assets/icons/${props.name}.svg`]()
    icon.value = rawIcon
  } catch {
    console.error(
      `[nuxt-icons] Icon '${props.name}' doesn't exist in 'assets/icons'`,
    )
  }
})
</script>

<style lang="scss" scoped>
.ui-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 1em;
    height: 1em;
    vertical-align: middle;
  }

  &--fill {
    fill: currentColor !important;
  }
}
</style>
