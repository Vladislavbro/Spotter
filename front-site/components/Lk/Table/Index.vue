<template>
  <table class="lk-table">
    <thead>
      <tr>
        <th
          v-for="(item, i) in filteredArray"
          :key="i"
        >
          <div class="lk-table__col">
            {{ item.label }}

            <LkTooltip
              v-if="item.info"
              :text="item.info"
              class="lk-table__info"
            />
          </div>
        </th>
      </tr>
    </thead>

    <slot />
  </table>
</template>

<script setup>
const props = defineProps({
  headColumns: {
    type: Array,
    default: () => ([]),
  },
})

const filteredArray = computed(() => {
  return props.headColumns.filter(item => item.show)
})
</script>

<style lang="scss" scoped>
.lk-table {
  width: 100%;
  text-align: left;

  &__col {
    display: flex;
    align-items: center;
  }

  &__info {
    margin-left: 4px;
  }

  thead {
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;
    background: #F8F8F9;
  }

  th {
    padding: 16px;
  }

  ::v-deep(tbody) {
    font-size: 15px;
    line-height: 18px;

    tr {
      border-top: 1px solid #E9E9EA;

      &:hover {
        background: #F8F8F9;
      }

      &:first-child {
        border-top: 0;
      }
    }

    td {
      padding: 16px;
    }
  }
}
</style>
