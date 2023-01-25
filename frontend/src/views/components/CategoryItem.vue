<template>
  <div class="">
    <div class="d-flex align-items-center category mb-1">
      <div v-if="category.children.length">
        <button
          class="btn btn-link p-0"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapse-' + category._id.$oid"
          aria-expanded="false"
          :aria-controls="'collapse-' + category._id.$oid">
          {{ category.name }}
        </button>
        <div class="collapse pt-2" :id="'collapse-' + category._id.$oid">
          <div
            v-for="child in category.children"
            :key="child._id.$oid"
            class="mb-1 ps-4">
            <CategoryItem :category="child"/>
          </div>
        </div>
      </div>
      <div v-else>
        <router-link :to="{name: 'Category', params: {id: category._id.$oid}}">
          {{ category.name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import CategoryItem from './CategoryItem'
export default {
  props: {
    category: Object
  },
  components: {
    CategoryItem
  }
}
</script>

<style lang="scss" scoped>
.category{
  .btn-group{
    visibility: hidden;
  }
  &:hover{
    .btn-group{
      visibility: visible;
    }
  }
}
</style>
