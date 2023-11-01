<template>
  <div class="profile">
    <div class="container-lk container-lk--profile">
      <div class="profile__box">
        <div class="profile__user">
          <LkUserProfile class="profile__profile" />

          <div
            v-if="user?.customer__subscribe_type"
            class="profile__tarif profile-tarif"
          >
            <div class="profile-tarif__info">
              <p class="profile-tarif__label">
                Тариф: {{ user.customer__subscribe_type === 'premium' ? 'Продвинутый' : user.customer__subscribe_type === 'trial' ? 'Базовый' : '--' }}
              </p>
              <p class="profile-tarif__date">
                Действует до {{ user.customer__subscribe_until || '--' }}
                <!-- Действует до 16.07.2023 -->
              </p>
            </div>

            <div class="profile-tarif__box">
              <p class="profile-tarif__price">
                1990 ₽
                <span>
                  / за месяц
                </span>
              </p>

              <UILkButton
                to="/lk/subscribes"
                text="Изменить тариф"
                primary-green
              />
            </div>
          </div>

          <div class="profile__history profile-history">
            <div class="profile-history__header">
              <div class="profile-history__row">
                <div
                  v-for="(item, i) in historyHead"
                  :key="i"
                  class="profile-history__col"
                >
                  {{ item }}
                </div>
              </div>
            </div>
            <div
              v-if="history.length"
              class="profile-history__body"
            >
              <div
                v-for="(item, i) in history"
                :key="i"
                class="profile-history__row"
              >
                <div class="profile-history__col">
                  {{ item.id }}
                </div>
                <div class="profile-history__col">
                  {{ dateFormat(item.date) }}
                </div>
                <div class="profile-history__col">
                  {{ item.subscribe_type === 'premium' ? 'Премиум' : item.subscribe_type === 'trial' ? 'Базовый' : '--' }}
                </div>
                <div class="profile-history__col">
                  до {{ dateFormat(item.date, 30) }}
                </div>
                <div class="profile-history__col">
                  {{ item.amount }} ₽
                </div>
              </div>
            </div>
          </div>

          <a
            href="#"
            class="profile__subscribe-cancel"
            @click.prevent="isShowCancelSubscribeModal = true"
          >
            Отменить подписку
          </a>
        </div>

        <CommonContactsBlock
          title="Будем рады вашей обратной связи"
          class="profile__contacts"
        />
      </div>
    </div>

    <ModalsLkCancelSubscribe
      v-if="isShowCancelSubscribeModal"
      @close="isShowCancelSubscribeModal = false"
    />
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { format, addDays } from 'date-fns'

import { useUserStore } from '@/store/user.js'

definePageMeta({
  layout: 'lk',
})

const { user } = storeToRefs(useUserStore())

console.log('user', user)

const isShowCancelSubscribeModal = ref(false)

const historyHead = ['#', 'Дата покупки', 'Тариф', 'Действует', 'Сумма']
const history = ref([])

const dateFormat = (date, days) => {
  let normalDate = date * 1000

  if (days) {
    normalDate = addDays(new Date(normalDate), days)
  }
  return format(normalDate, 'dd.MM.yyyy')
}

const getHistory = async () => {
  const { data } = await useFetch(`/api/account/${user?.value?.id}/orders`)

  history.value = data?.value?.orders || []
}

await getHistory()
</script>

<style lang="scss" scoped>
.profile {
  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 60px;
  }

  &__user {
    width: 100%;
    max-width: 720px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  &__profile, &__tarif {
    margin-bottom: 28px;
  }

  &__history {
    margin-bottom: 32px;
  }

  &__subscribe-cancel {
    color: var(--red);
    font-weight: 500;
    font-size: 15px;
    line-height: 18px;
  }

  &__contacts {
    margin-top: 80px;
  }
}

.profile-tarif {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32px 40px;
  color: var(--white);
  background: var(--blackMain);
  border-radius: 12px;

  &__info {
    display: flex;
    flex-direction: column;
  }

  &__label {
    margin-bottom: 4px;
    font-size: 20px;
    line-height: 24px;
  }

  &__date {
    color: var(--grayLight);
    font-size: 14px;
    line-height: 18px;
  }

  &__box {
    display: flex;
    align-items: center;
  }

  &__price {
    display: flex;
    align-items: baseline;
    margin-right: 20px;
    font-weight: 500;
    font-size: 28px;
    line-height: 36px;

    span {
      margin-left: 4px;
      font-weight: 500;
      font-size: 14px;
      line-height: 16px;
    }
  }
}

.profile-history {
  width: 100%;
  padding: 24px 40px 32px;
  background: var(--white);
  border-radius: 12px;

  &__header {
    padding-bottom: 14px;
    color: var(--grayLight);
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    border-bottom: 1px solid #E2E2E7;
  }

  &__row {
    display: grid;
    grid-template-columns: 48px repeat(4, 120px);
    grid-gap: 28px;
  }

  &__body {
    display: grid;
    grid-gap: 20px;
    padding-top: 20px;
    font-size: 14px;
    line-height: 18px;

    .profile-history {
      &__col {
        &:last-child {
          font-weight: 600;
        }
      }
    }
  }
}
</style>
