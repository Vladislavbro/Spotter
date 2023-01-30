<template lang="html">
  <div class="">
    <div class="display-1 text-center bg-light py-4">
      Аккаунт
    </div>

    <div class="container py-4">

      <div class="row">
        <div class="col">
          <div class="card card-body">
            <div class="mb-3">
              <label for="account-username-input">Логин</label>
              <input v-model="$store.state.user.username" readonly id="account-username-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-email-input">Email</label>
              <input type="email" v-model="$store.state.user.email" readonly id="account-email-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-first_name-input">Имя</label>
              <input v-model="$store.state.user.first_name" id="account-first_name-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-first_name-input">Фамилия</label>
              <input v-model="$store.state.user.last_name" id="account-last_name-input" class="form-control">
            </div>
            <button class="btn btn-primary me-3" @click="saveAccount">Сохранить</button>
          </div>
          "Что можно посмотреть:

      тарифы: пробный и премиум (названия пока под вопросом)

      Что можно сделать:
      - Изменить статус подписки с переходом на оплату от тинька"
        </div>
        <div class="col">
          <div class="card card-body">
            <p>
              Текущая подписка:
              <strong v-if="$store.state.user.customer__subscribe_type">{{ $store.state.user.customer__subscribe_type }}</strong>
            </p>
            <p class="text-secondary" v-if="$store.state.user.customer__subscribe_type">
              Заканчивается:
              {{ moment($store.state.user.customer__subscribe_until * 1000).fromNow() }}
            </p>

            <div class="row">
              <div class="col">
                <div class="card text-center">
                  <div class="card-header">
                    Пробная
                  </div>
                  <div class="card-body">
                    <h5 class="card-title"><i>69 ₽</i></h5>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <!-- <button @click="goToPay('trial', 69)" class="btn btn-warning btn-lg">Перейти</button> -->

                    <form ref="form" name="TinkoffPayForm text-center" @submit.prevent="tinkoffPayFunction">
                      <input class="tinkoffPayRow" type="hidden" name="terminalkey" value="1664189383150DEMO">
                      <input class="tinkoffPayRow" type="hidden" name="frame" value="true">
                      <input class="tinkoffPayRow" type="hidden" name="language" value="ru">
                      <input v-model="receipt" class="tinkoffPayRow" type="hidden" name="receipt">
                      <input class="tinkoffPayRow" type="hidden" value="69" placeholder="Сумма заказа" name="amount" required>
                      <!-- <input class="tinkoffPayRow" type="hidden" value="69" placeholder="Номер заказа" name="order"> -->
                      <input class="tinkoffPayRow" type="hidden" value="Переход на тариф Пробный" placeholder="Описание заказа" name="description">
                      <input v-model="name" class="tinkoffPayRow" type="hidden" placeholder="ФИО плательщика" name="name">
                      <input v-model="email" class="tinkoffPayRow" type="hidden" placeholder="E-mail" name="email">
                      <input v-model="phone" class="tinkoffPayRow" type="hidden" placeholder="Контактный телефон" name="phone">
                      <input type="submit" value="Перейти"  class="btn btn-warning btn-lg tinkoffPayRow">
                    </form>
                  </div>
                  <!-- <div class="card-footer text-muted">
                    2 days ago
                  </div> -->
                </div>
              </div>
              <div class="col">
                <div class="card text-center">
                  <div class="card-header">
                    Премиум
                  </div>
                  <div class="card-body">
                    <h5 class="card-title"><i>99 ₽</i></h5>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <button @click="goToPay('premium', 99)" class="btn btn-dark btn-lg">Перейти</button>
                  </div>
                  <!-- <div class="card-footer text-muted">
                    2 days ago
                  </div> -->
                </div>
              </div>
            </div>
          </div>

          <!-- <form ref="form" name="TinkoffPayForm" @submit.prevent="tinkoffPayFunction">
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
          </form> -->
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import moment from 'moment'
moment.locale('ru')
export default {
  data () {
    return {
      name: null,
      email: null,
      phone: null,
      amount: null,
      receipt: null,
    }
  },
  created: function () {
    this.moment = moment
  },
  methods: {
    goToPay (type, amount) {
      console.log('goToPay', type, amount)
      this.amount = amount
      this.email = this.$store.state.user.email
      this.name = `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`
      this.phone = '9099099099'
      if (this.amount && this.email && this.phone) {
        this.receipt = JSON.stringify({
          "Email": this.email,
          "Phone": this.phone,
          "EmailCompany": "mail@mail.com",
          "Taxation": "usn_income",
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
    },
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
  },
  mounted () {
    this.email = this.$store.state.user.email
    this.name = `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`
    this.phone = '9099099099'
  }
}
</script>

<style lang="css" scoped>
.tinkoffPayRow{display:block;margin:1%;width:160px;}
</style>
