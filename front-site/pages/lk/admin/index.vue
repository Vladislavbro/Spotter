<template>
  <div class="admin">
    <div class="container-lk">
      <div class="admin__box">
        <div class="admin__user">
          <LkUserProfile />
        </div>

        <div class="admin__content">
          <h1 class="admin__title">
            Аккаунты
          </h1>

          <div class="admin__header">
            <div class="admin__header-left">
              <div class="admin__search admin-search">
                <span class="admin-search__loop">
                  <UIBaseIcon name="landing/icon-loop" />
                </span>
                <UIBaseInput
                  v-model="search"
                  placeholder="Найти пользователя"
                  class="admin-search__input"
                />
              </div>

              <UILkButton
                text="+ Добавить аккаунт"
                @click="isShowAddUserModal = true"
              />
            </div>

            <!-- <LkTableSort
              :array="headColumns"
              class="admin__sort"
            /> -->
          </div>

          <div class="admin__list">
            <LkTable
              :head-columns="headColumns"
              class="admin__table admin-table"
            >
              <tbody class="admin-table__body">
                <tr
                  v-for="item in filteredAccounts"
                  :key="item.id"
                  class="admin-table__row"
                >
                  <td
                    v-if="headColumns[0].show"
                    class="admin-table__col"
                  >
                    <p class="admin-table-user">
                      {{ userFullname(item.first_name, item.last_name) }}
                      <span
                        v-if="item.is_superuser"
                        class="admin-table-user__type"
                      >
                        админ
                      </span>
                    </p>
                  </td>
                  <td
                    v-if="headColumns[1].show"
                    class="admin-table__col"
                  >
                    {{ item.email || '--' }}
                  </td>
                  <!-- <td class="admin-table__col">
                    {{ item.phone }}
                  </td>
                  <td class="admin-table__col">
                    {{ item.password }}
                  </td> -->
                  <td
                    v-if="headColumns[2].show"
                    class="admin-table__col"
                  >
                    <a
                      href="#"
                      class="admin-table__status admin-table-status"
                      @click.prevent="editableItem = item, isShowEditUserSubscribeModal = true"
                    >
                      <span :class="['admin-table-status__type', { 'admin-table-status__type--pro' : item.status === 'premium' }]" />
                      {{ item.customer__subscribe_type === 'premium' ? 'Продвинутый' : item.customer__subscribe_type === 'trial' ? 'Базовый' : '--' }}
                      <UIBaseIcon name="lk/icon-pencil" />
                    </a>
                  </td>
                  <td
                    v-if="headColumns[3].show"
                    class="admin-table__col"
                  >
                    <p class="admin-table-date">
                      {{ item.customer__subscribe_until || '--' }}
                      <!-- <span class="admin-table-date__time">
                        {{ item.time }}
                      </span> -->
                    </p>
                  </td>
                  <td class="admin-table__col">
                    <a
                      href="#"
                      class="admin-table-action"
                      @click.prevent="editableItem = item, isShowRemoveUserModal = true"
                    >
                      <UIBaseIcon name="lk/icon-trash" />
                    </a>
                  </td>
                </tr>
              </tbody>
            </LkTable>
          </div>
        </div>
      </div>
    </div>

    <ModalsLkAddUser
      v-if="isShowAddUserModal"
      @success="addNewUser"
      @close="isShowAddUserModal = false"
    />

    <ModalsLkRemoveUser
      v-if="isShowRemoveUserModal"
      :item="editableItem"
      @success="removeUser"
      @close="isShowRemoveUserModal = false"
    />

    <ModalsLkEditUserSubscribe
      v-if="isShowEditUserSubscribeModal"
      :item="editableItem"
      @success="editUser"
      @close="isShowEditUserSubscribeModal = false"
    />
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'lk',
})

const search = ref('')
const sortBy = ref('asc')

const accounts = ref([])

const isShowAddUserModal = ref(false)
const isShowRemoveUserModal = ref(false)
const isShowEditUserSubscribeModal = ref(false)
const editableItem = ref(null)

const headColumns = ref([
  { label: 'Имя, фамилия', show: true },
  { label: 'E-mail', show: true },
  // { label: 'Номер телефона', show: true },
  // { label: 'Пароль', show: true },
  { label: 'Статус подписки', show: true },
  { label: 'Подписка до', show: true },
  { label: '', show: true },
])

const filteredAccounts = computed(() => {
  const value = search.value.toLowerCase()

  if (value) {
    return accounts.value.filter((item) => {
      return item.first_name.toLowerCase().includes(value) || item.last_name.toLowerCase().includes(value)
    })
  }

  return accounts.value
})

const addNewUser = async (form) => {
  const { data } = await useFetch('/api/account', {
    method: 'post',
    body: form,
    headers: useHeaderToken(),
  })

  if (data?.value) {
    accounts.value.push(data.value)
  }
}

const editUser = (data) => {
  accounts.value.find((item, i) => {
    if (item.id === data.id) {
      accounts.value[i] = {
        ...item,
        ...data,
      }
      return true
    }

    return false
  })

  editableItem.value = null
}

const removeUser = async (id) => {
  editableItem.value = null

  const { data, error } = await useFetch(`/api/account/${id}/delete`, {
    method: 'delete',
    headers: useHeaderToken(),
  })

  const isNotValid = error?.value?.status
  if (isNotValid) {
    return false
  }

  accounts.value.find((item, i) => {
    if (+item.id === +id) {
      accounts.value.splice(i, 1)
      return true
    }

    return false
  })
}

const userFullname = (firstName, lastName) => {
  let fullName = '--'
  if (firstName) {
    fullName = firstName
  }
  if (lastName) {
    fullName += ` ${lastName}`
  }

  return fullName
}

const getUsers = async () => {
  const { data } = await useFetch('/api/accounts')

  accounts.value = data?.value?.accounts || []
}

await getUsers()
</script>

<style lang="scss" scoped>
.admin {
  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 100px;
  }

  &__user {
    width: 100%;
    max-width: 720px;
  }

  &__content {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-top: 80px;
  }

  &__title {
    margin-bottom: 20px;
    font-weight: 600;
    font-size: 32px;
    line-height: 40px;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;

    &-left {
      display: flex;
      align-items: center;
      flex: 1 1 auto;
    }
  }

  &__search {
    margin-right: 20px;
  }

  &__sort {
    ::v-deep(.lk-sort__box) {
      background: #fff;
    }
  }

  &__list {
    padding: 24px 24px 20px 20px;
    background: var(--white);
    border-radius: 12px;
  }
}

.admin-search {
  position: relative;
  width: 100%;
  max-width: 600px;

  &__loop {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 20px;
    display: flex;
    align-items: center;
    z-index: 1;

    ::v-deep(.ui-icon) {
      svg {
        width: 16px;
        height: 16px;

        & > * {
          fill: var(--grayLight);
        }
      }
    }
  }

  &__input {
    ::v-deep(.input__area) {
      height: 48px;
      padding: 15px 44px;
      line-height: 18px;
      border-radius: 8px;
    }
  }
}

.admin-table {
  width: 100%;
  text-align: left;

  &__body {
    font-size: 14px;
    line-height: 18px;
  }

  &__row {
    border-bottom: 1px solid #E9E9EA;

    &:hover {
      background: #F8F8F9;
    }
  }

  &__col {
    padding: 12px;
  }
}

.admin-table-user {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  grid-gap: 2px;

  &__type {
    display: block;
    padding: 4px 8px;
    font-size: 11px;
    line-height: 14px;
    color: var(--white);
    background: #8557E5;
    border-radius: 60px;
  }
}

.admin-table-status {
  display: grid;
  grid-gap: 8px;
  grid-template-columns: repeat(3, auto);
  align-items: center;
  justify-content: flex-start;
  font-weight: 500;

  &:hover {
    color: #8557E5;

    ::v-deep(.ui-icon) {
      svg {
        path {
          fill: #8557E5;
        }
      }
    }
  }

  &__type {
    width: 8px;
    height: 8px;
    background: #D9D9E0;
    border-radius: 50%;

    &--pro {
      background: var(--lime);
    }
  }
}

.admin-table-date {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  grid-gap: 2px;
  font-weight: 500;

  &__time {
    color: var(--grayLight);
    font-size: 13px;
    line-height: 16px;
  }
}

.admin-table-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;

  &:hover {
    ::v-deep(.ui-icon) {
      svg {
        path {
          fill: #8557E5;
        }
      }
    }
  }
}
</style>
