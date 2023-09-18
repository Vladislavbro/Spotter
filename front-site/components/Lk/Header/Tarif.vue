<template>
  <NuxtLink
    v-if="user?.customer__subscribe_type"
    to="/lk/subscribes"
    class="header-tarif"
  >
    <span class="header-tarif__discount">
      скидка 20%
    </span>
    Тариф Продвинутый
    <span class="header-tarif__date">
      до 02.03.2023
    </span>
  </NuxtLink>
</template>

<script setup>
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user.js'

const { user } = storeToRefs(useUserStore())
</script>

<style lang="scss" scoped>
.header-tarif {
  display: flex;
  align-items: center;
  padding: 6px 20px 6px 8px;
  font-size: 14px;
  line-height: 18px;
  background: var(--blackMain);
  border-radius: 120px;

  &--current {
    padding: 6px 20px;
    color: var(--blackMain);
    background: #F3F4F5;

    .header-tarif {
      &__date {
        color: var(--grayLight);
      }
    }
  }

  &__discount {
    margin-right: 12px;
    padding: 2px 8px;
    font-size: 12px;
    line-height: 14px;
    color: var(--blackMain);
    background: var(--lime);
    border-radius: 60px;
  }

  &__date {
    margin-left: 4px;
    color: #A7A7AB;
  }
}
</style>
