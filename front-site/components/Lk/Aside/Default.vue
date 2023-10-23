<template>
  <div class="aside">
    <ul class="aside__menu">
      <li
        v-for="(item, i) in menu"
        :key="i"
        class="aside__item aside-item"
      >
        <NuxtLink
          :to="item.link"
          class="aside-item__link"
        >
          <span
            v-if="item.icon"
            class="aside-item__icon"
          >
            <UIBaseIcon :name="`lk/${item.icon}`" />
          </span>
          {{ item.name }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user'

const { isAdmin } = storeToRefs(useUserStore())

const menu = [
  { name: 'Топ ниши', link: '/lk', icon: 'icon-star' },
  // { name: 'Категории', link: '/lk/category', icon: 'icon-category' },
  // { name: 'Продавцы', link: '/lk/sellers', icon: 'icon-users' },
  { name: 'Тарифы', link: '/lk/subscribes', icon: 'icon-card' },
]

const addToMenu = () => {
  if (isAdmin.value) {
    menu.push({ name: 'Админка', link: '/lk/admin', icon: '' })
  }
}

addToMenu()
</script>

<style lang="scss" scoped>
.aside {
  position: fixed;
  top: 72px;
  bottom: 0;
  left: 0;
  width: 120px;
  padding: 40px 8px;
  color: var(--white);
  background: var(--blackMain);
  z-index: 100;

  &__menu {
    display: grid;
    grid-gap: 12px;
  }
}

.aside-item {
  &__link {
    display: grid;
    grid-gap: 16px;
    justify-content: center;
    padding: 24px 0px 28px;
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;
    border-radius: 8px;

    &.router-link-exact-active, &:hover {
      color: #A7A7AF;
      background: #303038;

      ::v-deep(.ui-icon) {
        svg {
          path {
            fill: #A7A7AF;
          }
        }
      }
    }
  }
}
</style>
