<template lang="html">
  <div class="container py-5">
    Аккаунт
    <form name="TinkoffPayForm" onsubmit="pay(this); return false;">
      <input class="tinkoffPayRow" type="hidden" name="terminalkey" value="1664189383150DEMO">
      <input class="tinkoffPayRow" type="hidden" name="frame" value="true">
      <input class="tinkoffPayRow" type="hidden" name="language" value="ru">
      <input class="tinkoffPayRow" type="text" placeholder="Сумма заказа" name="amount" required>
      <input class="tinkoffPayRow" type="text" placeholder="Номер заказа" name="order">
      <input class="tinkoffPayRow" type="text" placeholder="Описание заказа" name="description">
      <input class="tinkoffPayRow" type="text" placeholder="ФИО плательщика" name="name">
      <input class="tinkoffPayRow" type="text" placeholder="E-mail" name="email">
      <input class="tinkoffPayRow" type="text" placeholder="Контактный телефон" name="phone">
      <input class="tinkoffPayRow" type="submit" value="Оплатить">
    </form>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css" scoped>
.tinkoffPayRow{display:block;margin:1%;width:160px;}
</style>
