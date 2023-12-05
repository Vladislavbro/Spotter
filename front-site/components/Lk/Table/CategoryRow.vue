<template>
  <tr :class="{ 'category-row--active' : isShow }">
    <td>
      <a
        href="#"
        :style="`padding-left: ${32 * index}px`"
        class="category-row__name"
        @click.prevent="item.items.length ? isShow = !isShow : ''"
      >
        <span
          v-if="item.items.length"
          class="category-row__arrow"
        >
          <UIBaseIcon name="lk/icon-arrow-down" />
        </span>
        {{ item.name }}
      </a>
    </td>
    <td>
      {{ productsCount.toLocaleString() }}
    </td>
    <td>
      {{ sellersCount.toLocaleString() }}
    </td>
    <td>
      {{ profit.toLocaleString() }}
    </td>
    <td>
      {{ priceAvg.toLocaleString() }}
    </td>
    <td>
      {{ sellersSolded.toLocaleString() }}
    </td>
    <td>
      {{ productsSolded.toLocaleString() }}
    </td>
  </tr>

  <template v-if="item.items.length && isShow">
    <LkTableCategoryRow
      v-for="(child, c) in item.items"
      :key="c"
      :item="child"
      :index="index + 1"
    />
  </template>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  index: {
    type: Number,
    default: 0,
  },
})

const isShow = ref(false)

const stat = computed(() => {
  if (props?.item?.stat?.length) {
    return props?.item?.stat[0]
  }

  return null
})

const productsCount = computed(() => {
  return stat.value?.products_count || ''
})

const sellersCount = computed(() => {
  return stat.value?.sellers_count || ''
})

const profit = computed(() => {
  return stat.value?.profit || ''
})

const priceAvg = computed(() => {
  return stat.value?.price_avg || ''
})

const sellersSolded = computed(() => {
  return stat.value?.sellers_solded || ''
})

const productsSolded = computed(() => {
  return stat.value?.products_solded || ''
})
</script>

<style lang="scss" scoped>
.category-row {
  &--hide {
    display: none;
  }

  &--active {
    .category-row {
      &__name {
        color: #9D9DA5;
      }

      &__arrow {
        .ui-icon {
          transform: rotate(180deg);
        }
      }
    }
  }

  &__name {
    display: flex;
    align-items: center;
    grid-gap: 8px;

    font-weight: 500;
    font-size: 14px;
  }

  &__arrow {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 24px;
    height: 24px;

    border: 1px solid var(--gray-light, #E2E2E7);
    border-radius: 4px;

    .ui-icon {
      transition: transform 0.3s;
    }

    ::v-deep(.ui-icon) svg {
      & > * {
        fill: #000;
      }
    }
  }
}
</style>
