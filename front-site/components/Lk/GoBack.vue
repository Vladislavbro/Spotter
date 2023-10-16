<template>
  <a
    :href="link"
    class="go-back"
    @click.prevent="goTo()"
  >
    <span class="go-back__icon">
      <UIBaseIcon name="lk/icon-arrow-left" />
    </span>
    {{ text }}
  </a>
</template>

<script setup>
const props = defineProps({
  link: {
    type: String,
    default: '',
  },
  text: {
    type: String,
    default: '',
  },
})

const router = useRouter()

const goTo = () => {
  if (props.link) {
    return router.push(props.link)
  }

  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/lk')
  }
}
</script>

<style lang="scss" scoped>
.go-back {
  display: flex;
  align-items: center;
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    margin-right: 12px;
    background: var(--white);
    box-shadow: 0px 2px 6px rgba(44, 48, 64, 0.2);
    border-radius: 4px;
  }
}
</style>
