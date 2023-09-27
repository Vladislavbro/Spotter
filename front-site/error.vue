<template>
  <div class="error-page">
    <h1 v-if="error.statusCode === 404">
      Page not found 
    </h1>
    <h1 v-else-if="error.statusCode === 500">
      Internal Server error
    </h1>
    <h1 v-else>
      An error occurred
    </h1>

    <UIBaseButton
      to="/"
      primary-black-outline
      text="Home page"
    />
  </div>
</template>

<script setup>
defineProps({
  error: {
    type: Object,
    default: () => ({}),
  },
})

// const handleError = () => clearError({ redirect: '/' })
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  grid-gap: 20px;
  min-height: 100vh;
  padding: 100px 0;
  color: var(--blackMain);
  background: #F3F4F5;
}
</style>
