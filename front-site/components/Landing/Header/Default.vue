<template>
  <header class="header">
    <div class="container">
      <div class="header__box">
        <div class="header__left-side">
          <CommonLogo class="header__logo" />

          <nav class="header__menu menu">
            <ul class="menu__list">
              <li v-for="(item, i) in menuList" :key="i" class="menu__item">
                <a :href="item.link" class="menu__link">
                  {{ item.label }}
                </a>
              </li>
            </ul>
          </nav>
        </div>

        <div class="header__btns">
          <UIBaseButton
            v-if="isAuth"
            to="/lk/profile"
            text="Личный кабинет"
            class="header__btn"
          />

          <template v-else>
            <UIBaseButton
              to="/sign-in"
              text="Войти"
              class="header__btn"
            />

            <UIBaseButton
              to="/sign-up"
              text="Зарегистрироваться"
              primary-green-outline
              class="header__btn header__btn--sign-up"
            />
          </template>

          <button
            :class="['header__btn header__btn--burger burger', { 'burger--active' : isMobileMenu }]"
            @click.prevent="isMobileMenu = !isMobileMenu"
          >
            <span class="burger__box">
              <span />
            </span>
          </button>
        </div>
      </div>
    </div>

    <div :class="['mobile-menu', { 'mobile-menu--open' : isMobileMenu }]">
      <div class="mobile-menu__box">
        <ul class="mobile-menu__list">
          <li
            v-for="(item, i) in menuList"
            :key="i"
            class="mobile-menu__item"
          >
            <a
              href="#"
              class="mobile-menu__link"
              @click.prevent="linkInMobileMenu('/')"
            >
              {{ item.label }}
            </a>
          </li>
        </ul>

        <div class="mobile-menu__btns">
          <UIBaseButton
            v-if="isAuth"
            text="Личный кабинет"
            class="mobile-menu__btn"
            @click="linkInMobileMenu('/lk/profile')"
          />

          <template v-else>
            <UIBaseButton
              text="Войти"
              class="mobile-menu__btn"
              @click="linkInMobileMenu('/sign-in')"
            />

            <UIBaseButton
              text="Зарегистрироваться"
              primary-green-outline
              class="mobile-menu__btn mobile-menu__btn--sign-up"
              @click="linkInMobileMenu('/sign-up')"
            />
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/user'

const { isAuth } = storeToRefs(useUserStore())
const router = useRouter()

const isMobileMenu = ref(false)

const menuList = [
  { label: 'Возможности', link: '#opportunity' },
  { label: 'Как пользоваться', link: '#how-to-use' },
  { label: 'Отзывы', link: '#reviews' },
  { label: 'Тарифы', link: '#tarifs' },
  { label: 'Контакты', link: '#contacts' },
]

const linkInMobileMenu = (link) => {
  isMobileMenu.value = false
  router.push(link)
}
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  background: var(--blackMain);
  border-bottom: 1px solid var(--blackLight);
  z-index: 100;

  &__box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
  }

  &__left-side {
    display: flex;
    align-items: center;
  }

  &__menu {
    @include mq($bp-medium) {
      margin-left: 20px;
    }

    @include mq($bp-big) {
      margin-left: 40px;
    }
  }

  &__btns {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
    align-items: center;

    @include mq($bp-small-medium) {
      grid-gap: 16px;
    }

    @include mq($bp-medium) {
      grid-gap: 12px;
    }
  }

  &__btn {
    @include mq(0px, $bp-small-medium) {
      padding: 10px;

      font-size: 12px;
    }

    &--sign-up {
      display: none;

      @include mq($bp-medium) {
        display: block;
      }
    }

    &--burger {
      display: flex;
      z-index: 102;

      @include mq($bp-medium) {
        display: none;
      }
    }
  }
}

.menu {
  display: none;

  @include mq($bp-medium) {
    display: block;
  }

  &__list {
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(5, auto);

    @include mq($bp-big) {
      grid-gap: 40px;
    }
  }

  &__link {
    font-weight: 500;
    font-size: 14px;
    line-height: 22px;

    @include mq($bp-big) {
      font-size: 16px;
    }

    &:hover {
      color: var(--lime);
    }
  }
}

.burger {
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 1px;

  &--active {
    .burger {
      &__box {
        &:before {
          animation: 0.3s linear 0s burger_top_line_active forwards;
        }

        &:after {
          animation: 0.3s linear 0s burger_bottom_line_active forwards;
        }

        span {
          opacity: 0;
        }
      }
    }
  }

  &__box {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    height: 16px;

    &:before, &:after {
      content: '';
    }

    &:before, &:after, span {
      width: 100%;
      height: 2px;
      background: var(--white);
    }

    &:before {
      animation: 0.3s linear 0s burger_top_line forwards;
    }

    &:after {
      animation: 0.3s linear 0s burger_bottom_line forwards;
    }

    span {
      opacity: 1;
      transition: opacity 0s linear 0.15s;
    }
  }
}

.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  max-height: 0%;
  background: var(--blackMain);
  overflow: hidden;
  transition: max-height 0.3s;
  z-index: 101;

  &--open {
    max-height: 100%;
  }

  &__box {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 104px 20px 60px;
    overflow-y: auto;
  }

  &__list {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  &__link {
    display: block;
    padding: 16px 0;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    text-align: center;

    &:hover {
      color: var(--lime);
    }
  }

  &__btns {
    display: flex;
    flex-direction: column;
    align-items: center;
    grid-gap: 16px;
    margin-top: 32px;
  }

  &__btn {
    padding: 12px 24px;
  }
}

@keyframes burger_top_line_active {
  0% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(7px) rotate(0deg);
  }
  100% {
    transform: translateY(7px) rotate(45deg);
  }
}

@keyframes burger_bottom_line_active {
  0% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-7px) rotate(0deg);
  }
  100% {
    transform: translateY(-7px) rotate(-45deg);
  }
}

@keyframes burger_top_line {
  0% {
    transform: translateY(7px) rotate(45deg);
  }
  50% {
    transform: translateY(7px) rotate(0deg);
  }
  100% {
    transform: translateY(0px) rotate(0deg);
  }
}

@keyframes burger_bottom_line {
  0% {
    transform: translateY(-7px) rotate(-45deg);
  }
  50% {
    transform: translateY(-7px) rotate(0deg);
  }
  100% {
    transform: translateY(0px) rotate(0deg);
  }
}
</style>
