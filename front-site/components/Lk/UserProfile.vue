<template>
  <div class="user-profile">
    <div class="user-profile__info">
      <div class="user-profile__avatar">
        <UIBaseIcon name="lk/icon-user" />
      </div>
      <p class="user-profile__fullname">
        {{ fullName }}
      </p>
      <a
        href="#"
        class="user-profile__logout"
        @click.prevent="logOut()"
      >
        Выйти из аккаунта
      </a>
    </div>

    <div class="user-profile__contacts">
      <div
        v-if="user && user.customer__phone"
        class="user-profile__line"
      >
        <div class="user-profile__box">
          <div class="user-profile__icon">
            <UIBaseIcon name="lk/icon-phone" />
          </div>
          <div class="user-profile__content">
            <p class="user-profile__label">
              Телефон
            </p>
            <p class="user-profile__value">
              {{ user.customer__phone }}
            </p>
          </div>
        </div>
      </div>

      <!-- <div class="user-profile__line">
        <div class="user-profile__box">
          <div class="user-profile__icon">
            <UIBaseIcon name="lk/icon-mail" />
          </div>
          <div class="user-profile__content">
            <p class="user-profile__label">
              Username
            </p>
            <p class="user-profile__value">
              {{ user.username }}
            </p>
          </div>
        </div>
      </div> -->

      <div
        v-if="user && user.email"
        class="user-profile__line"
      >
        <div class="user-profile__box">
          <div class="user-profile__icon">
            <UIBaseIcon name="lk/icon-mail" />
          </div>
          <div class="user-profile__content">
            <p class="user-profile__label">
              Электронная почта
            </p>
            <p class="user-profile__value">
              {{ user.email }}
            </p>
          </div>
        </div>
      </div>

      <div class="user-profile__line">
        <div class="user-profile__box">
          <div class="user-profile__icon">
            <UIBaseIcon name="lk/icon-key" />
          </div>
          <div class="user-profile__content">
            <p class="user-profile__label">
              Пароль
            </p>
            <p class="user-profile__value">
              <!-- Изменен 3 месяца назад -->
            </p>
          </div>
        </div>

        <UILkButton
          to="/lk/change-password"
          text="Изменить пароль"
          primary-gray
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user.js'

const { userLogOut } = useUserStore()
const { user } = storeToRefs(useUserStore())

const fullName = computed(() => {
  return user?.value ? `${user.value.first_name} ${user.value.last_name}` : ''
})

const logOut = async () => {
  await userLogOut()
  navigateTo('/')
}
</script>

<style lang="scss" scoped>
.user-profile {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  &__info {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 32px;
  }

  &__avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    margin-bottom: 16px;
    background: var(--white);
    border-radius: 50%;
  }

  &__fullname {
    font-weight: 600;
    font-size: 28px;
    line-height: 36px;
    margin-bottom: 12px;
  }

  &__logout {
    font-weight: 500;
    font-size: 15px;
    line-height: 18px;
    color: var(--grayLight);
  }

  &__contacts {
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 40px;
    background: var(--white);
    border-radius: 12px;
  }

  &__line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 24px;

    &:first-child {
      margin-top: 0;
    }
  }

  &__box {
    display: flex;
    align-items: center;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    margin-right: 12px;
    background: #F3F4F5;
    border-radius: 50%;
  }

  &__content {
    display: flex;
    flex-direction: column;
  }

  &__label {
    margin-bottom: 4px;
    font-size: 14px;
    line-height: 18px;
    color: var(--grayLight);
  }

  &__value {
    font-weight: 600;
    line-height: 20px;
  }
}
</style>
