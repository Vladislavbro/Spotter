<template>
  <div class="container py-4">
    {{ $store.state.category }}
  </div>
</template>

<script>
export default {
  mounted () {
    const id = this.$route.params.id
    this.$store.dispatch('getCategory', id)
  }
}
</script>

<style lang="css" scoped>
</style>
