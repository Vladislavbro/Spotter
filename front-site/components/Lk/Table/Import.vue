<template>
  <button class="lk-import">
    <UIBaseIcon name="lk/icon-import" />
    Выгрузить в Excel
  </button>
</template>

<script setup></script>

<style lang="scss" scoped>
.lk-import {
  display: grid;
  grid-gap: 4px;
  grid-template-columns: repeat(2, auto);
  align-items: center;
  height: 44px;
  padding: 0 20px;
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;
  background: #F3F4F5;
  border-radius: 8px;

  &:hover {
    background: #e9eaec;
  }
}
</style>
