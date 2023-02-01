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
                    <h5 class="card-title"><i>19 ₽</i></h5>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <button @click="getOrder('trial', 19)" class="btn btn-warning btn-lg">Перейти</button>
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
                    <button @click="getOrder('premium', 29)" class="btn btn-dark btn-lg">Перейти</button>
                  </div>
                  <!-- <div class="card-footer text-muted">
                    2 days ago
                  </div> -->
                </div>
              </div>
            </div>
          </div>
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
      order: {},
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

    getToken (name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    async getOrder (subscribe_type, amount) {
      try {
        const response = await fetch('/api/order', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getToken('csrftoken'),
          },
          body: JSON.stringify({subscribe_type, amount})
        })
        const data = await response.json()
        console.log('data', data)
        if (data.order) {
          this.order = data.order
          this.goToPay(subscribe_type, amount)
        }
      } catch (e) {
        console.error(e)
      }
    },

    async goToPay (subscribe_type, amount) {
      try {
        const response = await fetch('https://securepay.tinkoff.ru/v2/Init', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            TerminalKey: '1664189383150',
            Amount: amount * 100,
            OrderId: this.order.id,
            Description: `Оформление подписки за ${amount}.00 рублей`,
            DATA: {
              Phone: this.$store.state.user.phone,
              Email: this.$store.state.user.email
            },
            Receipt: {
              Email: this.$store.state.user.email,
              Phone: this.$store.state.user.phone,
              EmailCompany: 'i.vladsn@gmail.com',
              Taxation: 'usn_income_outcome',
              Items: [
                {
                  Name: `Подписка ${subscribe_type}`,
                  Price: amount * 100,
                  Quantity: 1.00,
                  Amount: amount * 100,
                  PaymentMethod: 'full_prepayment',
                  PaymentObject: 'service',
                  Tax: 'none',
                  // Ean13: "0123456789"
                },
              ]
            }
          })
        })
        const data = await response.json()
        if (data.Success) {
          location.replace(data.PaymentURL)
        }
        console.log('data', data)
      } catch (e) {
        console.error(e)
      }
    },

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
