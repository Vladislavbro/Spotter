<template lang="html">
  <div class="container py-4">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Username</th>
          <th>email</th>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Подписка до</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="account in accounts" :key="account.id">
          <td>
            {{ account.username }}
            <span v-if="account.is_superuser" class="badge bg-primary">Админ</span>
          </td>
          <td>{{ account.email }}</td>
          <td>{{ account.first_name }}</td>
          <td>{{ account.last_name }}</td>
          <td>{{ moment(account.customer__subscribe_until * 1000).format() }}</td>
          <td>
            <button
              class="btn btn-link"
              @click="setAccount(account)"
              data-bs-toggle="modal"
              data-bs-target="#userModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info" viewBox="0 0 16 16">
                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div
      class="modal fade"
      id="userModal"
      tabindex="-1"
      aria-labelledby="titleUserModal"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="titleUserModal">
              Пользователь
              {{ account.username }}
              <span v-if="account.is_superuser" class="badge bg-primary">Админ</span>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="account-first_name-input">Имя</label>
              <input v-model="account.first_name" id="account-first_name-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-first_name-input">Фамилия</label>
              <input v-model="account.last_name" id="account-last_name-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-customer__subscribe_until-input">Подписка до</label>
              <input
                type="datetime-local"
                v-model="account.customer__subscribe_until"
                id="account-customer__subscribe_until-input"
                class="form-control">
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary me-3" @click="saveAccount">Сохранить</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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
      accounts: [],
      account: {},
    }
  },
  created: function () {
    this.moment = moment
  },
  methods: {
    async getAccounts () {
      try {
        const response = await fetch('/api/accounts')
        const data = await response.json()
        this.accounts = data.accounts
      } catch (e) {
        console.error(e)
        this.$toast.error(`${e.type}: ${e.message}`)
      }
    },
    setAccount (account) {
      this.account = {
        ...account,
        customer__subscribe_until: moment(account.customer__subscribe_until * 1000).format().substr(0, 16),
      }
    },
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
    async saveAccount () {
      try {
        let subscribe_until = this.account.customer__subscribe_until
        if (subscribe_until) {
          subscribe_until = moment(this.account.customer__subscribe_until).unix()
        }
        const response = await fetch('/api/account', {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getToken('csrftoken')
          },
          body: JSON.stringify({
            subscribe_until,
            id: this.account.id,
            first_name: this.account.first_name,
            last_name: this.account.last_name,
          })
        })
        const data = await response.json()
        console.log('data', data)
        this.account = data
        // this.$store.commit('mergeStore', {account: this.account})
        this.getAccounts()
      } catch (e) {
        console.error(e)
        this.$toast.error(`${e.type}: ${e.message}`)
      }
    },
  },
  mounted () {
    if (this.$store.state.user.is_superuser) {
      this.getAccounts()
    }
  }
}
</script>

<style lang="css" scoped>
</style>
