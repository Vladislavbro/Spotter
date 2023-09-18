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
      {{ item.products_count }}
    </td>
    <td>
      {{ item.sellers_count }}
    </td>
    <!-- <td>
      {{ item.brands_count }}
    </td> -->
    <td>
      {{ item.profit }}
    </td>
    <td>
      {{ item.price_avg }}
    </td>
    <td>
      {{ item.products_solded }}
    </td>
    <!-- <td>
      {{ item.brands }}
    </td> -->
    <td>
      {{ item.sellers_solded }}
    </td>
    <!-- <td>
      {{ item.average_sale_items }}
    </td> -->
    <!-- <td>
      {{ item.average_sale_sellers }}
    </td> -->
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
defineProps({
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
