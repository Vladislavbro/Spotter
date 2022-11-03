<template>
  <div class="container py-4">
    <h3>{{ $store.state.category.name }}</h3>
    <small>{{ $store.state.category }}</small>
    <div class="py-3 text-end">
      Товаров: <strong>{{ $store.state.info }}</strong>
    </div>
    <table class="table table-bordered table-hover">
      <thead>
        <th>Группа</th>
        <th>Товаров</th>
        <th>Продаж в предыдущей декаде</th>
        <th>Продаж в текущей декаде</th>
        <th>Процент роста</th>
      </thead>
      <tbody>
        <tr v-for="(group, i) in $store.state.groups" :key="i">
          <td>{{ group[0] }}</td>
          <td>{{ group[1] }}</td>
          <td>{{ group[2] }}</td>
          <td>{{ group[3] }}</td>
          <td>{{ group[4] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('mergeStore', {
      category: {},
      groups: [],
      info: null,
    })
    const id = this.$route.params.id
    this.$store.dispatch('getCategory', id)
  }
}
</script>

<style lang="css" scoped>
</style>
