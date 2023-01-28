<template lang="html">
  <div class="container py-5">
    Аккаунт
    <form ref="form" name="TinkoffPayForm" @submit.prevent="tinkoffPayFunction">
      <input class="tinkoffPayRow" type="hidden" name="terminalkey" value="1664189383150DEMO">
      <input class="tinkoffPayRow" type="hidden" name="frame" value="true">
      <input class="tinkoffPayRow" type="hidden" name="language" value="ru">
      <input v-model="receipt" class="tinkoffPayRow" type="hidden" name="receipt">
      <input v-model="amount" class="tinkoffPayRow" type="text" placeholder="Сумма заказа" name="amount" required>
      <input class="tinkoffPayRow" type="text" placeholder="Номер заказа" name="order">
      <input class="tinkoffPayRow" type="text" placeholder="Описание заказа" name="description">
      <input v-model="name" class="tinkoffPayRow" type="text" placeholder="ФИО плательщика" name="name">
      <input v-model="email" class="tinkoffPayRow" type="text" placeholder="E-mail" name="email">
      <input v-model="phone" class="tinkoffPayRow" type="text" placeholder="Контактный телефон" name="phone">
      <input class="tinkoffPayRow" type="submit" value="Оплатить">
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      name: 'Оплата',
      email: null,
      phone: null,
      amount: 100,
      receipt: null
    }
  },
  methods: {
    tinkoffPayFunction () {
      if (this.amount && this.email && this.phone) {
        this.receipt = JSON.stringify({
          "Email": this.email,
          "Phone": this.phone,
          "EmailCompany": "mail@mail.com",
          "Taxation": "patent",
          "Items": [
            {
              "Name": this.name,
              "Price": this.amount + '00',
              "Quantity": 1.00,
              "Amount": this.amount + '00',
              "PaymentMethod": "full_prepayment",
              "PaymentObject": "service",
              "Tax": "none"
            }
          ]
        })
        window.pay(this.$refs.form)
      } else {
        alert("Не все обязательные поля заполнены")
      }
      return false
    }
  }
}
</script>

<style lang="css" scoped>
.tinkoffPayRow{display:block;margin:1%;width:160px;}
</style>
