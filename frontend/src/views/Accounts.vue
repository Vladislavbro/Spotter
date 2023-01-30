<template lang="html">
  <div class="container py-4">
    <div class="d-flex mb-4">
      <h3>Аккаунты</h3>
      <div class="ms-auto">
        <button
          class="btn btn-light"
          @click="account = {}"
          data-bs-toggle="modal"
          data-bs-target="#userModal">
          Добавить новый аккаунт
        </button>
      </div>
    </div>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Username</th>
          <th>email</th>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Тип подписки</th>
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
          <td>{{ account.customer__subscribe_type }}</td>
          <td>
            <span v-if="account.customer__subscribe_until">
              {{ moment(account.customer__subscribe_until * 1000).format() }}
            </span>
          </td>
          <td class="text-end">
            <button
              class="btn btn-link"
              @click="setAccount(account)"
              data-bs-toggle="modal"
              data-bs-target="#userModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info" viewBox="0 0 16 16">
                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
              </svg>
            </button>
            <button
              class="btn btn-link"
              @click="deleteAccount(account)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"/>
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
            <div class="mb-3" v-if="!account.id">
              <label for="account-username-input">Логин</label>
              <input v-model="account.username" id="account-username-input" class="form-control">
            </div>
            <div class="mb-3" v-if="!account.id">
              <label for="account-email-input">Email</label>
              <input type="email" v-model="account.email" id="account-email-input" class="form-control">
            </div>
            <div class="mb-3" v-if="!account.id">
              <label for="account-password-input">Пароль</label>
              <input type="text" v-model="account.password" id="account-password-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-first_name-input">Имя</label>
              <input v-model="account.first_name" id="account-first_name-input" class="form-control">
            </div>
            <div class="mb-3">
              <label for="account-first_name-input">Фамилия</label>
              <input v-model="account.last_name" id="account-last_name-input" class="form-control">
            </div>
            <div class="row mb-3">
              <div class="col">
                <label for="account-customer__subscribe_type-select">Тип подписки</label>
                <select
                  v-model="account.customer__subscribe_type"
                  id="account-customer__subscribe_type-select"
                  class="form-control">
                  <option value="trial">Пробная</option>
                  <option value="premium">Премиум</option>
                </select>
              </div>
              <div class="col">
                <label for="account-customer__subscribe_until-input">Подписка до</label>
                <input
                  type="datetime-local"
                  v-model="account.customer__subscribe_until"
                  id="account-customer__subscribe_until-input"
                  class="form-control">
              </div>
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
            subscribe_type: this.account.customer__subscribe_type,
            id: this.account.id,
            first_name: this.account.first_name,
            last_name: this.account.last_name,
            username: this.account.username,
            password: this.account.password,
            email: this.account.email,
          })
        })
        console.log('response', response)
        if (response.status === 200) {
          this.$toast.success(`Успешно обновлено`)
          const data = await response.json()
          console.log('data', data)
          this.account = {
            ...data,
            customer__subscribe_until: this.moment(data.customer__subscribe_until * 1000).format().substr(0, 16)
          }
          // this.$store.commit('mergeStore', {account: this.account})
          this.getAccounts()
        } else {
          this.$toast.error(`Что то пошло не так`)
        }
      } catch (e) {
        console.error(e)
        this.$toast.error(`${e.type}: ${e.message}`)
      }
    },
    async deleteAccount (account) {
      try {
        if (confirm('Удалить аккаунт?')) {
          const response = await fetch(`/api/account/${account.id}/delete`, {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': this.getToken('csrftoken')
            }
          })
          if (response.status === 200) {
            this.$toast.success(`Успешно удалено`)
            this.getAccounts()
          } else {
            this.$toast.error(`Что то пошло не так`)
          }
        }
      } catch (e) {
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
