<template>
  <div
    v-click-outside="close"
    :class="['lk-sort', { 'lk-sort--white' : isWhite }]"
  >
    <div
      class="lk-sort__box"
      @click.prevent="isOpen = !isOpen"
    >
      <p class="lk-sort__side">
        <span class="lk-sort__label">
          Сортировка:
        </span>
        {{ label }}
      </p>

      <div class="lk-sort__actions">
        <a
          href="#"
          :class="['lk-sort__action lk-sort__action--asc', { 'lk-sort__action--active' : direction === 'asc'}]"
          @click.prevent.stop="direction = 'asc', change()"
        >
          <UIBaseIcon name="lk/icon-sort-arrow-down" />
        </a>
        <a
          href="#"
          :class="['lk-sort__action lk-sort__action--desc', { 'lk-sort__action--active' : direction === 'desc'}]"
          @click.prevent.stop="direction = 'desc', change()"
        >
          <UIBaseIcon name="lk/icon-sort-arrow-down" />
        </a>
      </div>
    </div>

    <div
      v-if="isOpen"
      class="lk-sort__dropdown"
    >
      <div class="lk-sort__list">
        <UILkRadio
          v-for="(item, i) in sortList"
          :id="item.slug"
          :key="i"
          v-model="slug"
          :text="item.label"
          :value="item.slug"
          class="lk-sort__item"
          @change="change()"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  array: {
    type: Array,
    default: () => ([]),
  },
  sortSlug: {
    type: String,
    default: '',
  },
  sortDirection: {
    type: String,
    default: 'asc',
  },
  isWhite: {
    type: Boolean,
    default: false,
  },
})

const emits = defineEmits(['change'])

const isOpen = ref(false)
const slug = ref(null)
const direction = ref(null)

const sortList = computed(() => {
  return props.array.filter(item => item.sort)
})

const label = computed(() => {
  return sortList.value.find(item => item.slug === props.sortSlug)?.label || ''
})

const close = () => {
  isOpen.value = false
}

const change = () => {
  emits('change', {
    slug: slug.value,
    direction: direction.value,
  })
}

const setDefault = () => {
  slug.value = props.sortSlug
  direction.value = props.sortDirection
}

setDefault()
</script>

<style lang="scss" scoped>
.lk-sort {
  position: relative;

  &--white {
    .lk-sort {
      &__box {
        background: var(--white);
        border: 1px solid #E2E2E7;
      }
    }
  }

  &__box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 290px;
    height: 44px;
    padding: 0 20px 0 16px;
    background: #F3F4F5;
    border: 1px solid #F3F4F5;
    border-radius: 8px;
    cursor: pointer;

    &:hover {
      border-color: #E2E2E7;
    }
  }

  &__side {
    display: flex;
    align-items: center;
    margin-right: 10px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__label {
    margin-right: 4px;
    color: #8B8B91;
  }

  &__actions {
    display: grid;
    grid-template-columns: repeat(2, auto);
    grid-gap: 4px;
  }

  &__action {
    &--asc {
      transform: rotate(180deg);
    }

    &--active {
      ::v-deep(.ui-icon) {
        svg {
          path {
            fill: var(--blackMain);
          }
        }
      }
    }
  }

  &__dropdown {
    position: absolute;
    top: calc(100% + 4px);
    right: 0;
    left: 0;

    background: var(--white);
    border: 1px solid #E2E2E7;
    box-shadow: 0px 4px 20px rgba(44, 48, 64, 0.12);
    border-radius: 8px;
    z-index: 100;
  }

  &__list {
    display: flex;
    flex-direction: column;
  }

  &__item {
    padding: 16px 20px;
    border-top: 1px solid #E9E9EA;

    &:first-child {
      border-top: 0;
    }
  }
}
</style>
