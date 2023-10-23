<template>
  <footer id="contacts" :class="['footer', { 'footer--light' : themeLight }]">
    <div :class="getContainerClass">
      <div class="footer__box">
        <div class="footer__col">
          <CommonLogo
            :is-black="themeLight"
            class="footer__logo"
          />

          <p class="footer__description">
            Spotter – это сервис с искусственным интеллектом, который собирает свободные ниши на&nbsp;Wildberries.
          </p>
        </div>

        <div class="footer__cols">
          <div class="footer__col">
            <p class="footer__label">
              О сервисе
            </p>
            <ul class="footer__list">
              <li
                v-for="(item, i) in menuList"
                :key="i"
                class="footer__item"
              >
                <NuxtLink
                  :to="item.link"
                  class="footer__link"
                >
                  {{ item.label }}
                </NuxtLink>
              </li>
            </ul>
          </div>

          <div class="footer__col">
            <p class="footer__label">
              Связаться с нами
            </p>
            <ul class="footer__list">
              <li
                v-for="(item, i) in contactsList"
                :key="i"
                class="footer__item"
              >
                <a
                  :href="item.link"
                  target="_blank"
                  class="footer__link"
                >
                  <span class="footer__icon">
                    <UIBaseIcon :name="item.icon" />
                  </span>
                  {{ item.label }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="footer__bottom">
      <div :class="getContainerClass">
        <div class="footer__line">
          <p class="footer__text">
            Spotter © 2023. Все права защищены
          </p>

          <div class="footer__rules">
            <NuxtLink to="/privacy" class="footer__text">
              Политика конфиденциальности
            </NuxtLink>
            <NuxtLink to="/privacy" class="footer__text">
              Пользовательское соглашение
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const props = defineProps({
  themeLight: {
    type: Boolean,
    default: false,
  },
  layout: {
    type: String,
    default: 'default',
  },
})

const menuList = [
  { label: 'Возможности', link: '/' },
  { label: 'Как пользоваться', link: '/' },
  { label: 'Отзывы', link: '/' },
  { label: 'Тарифы', link: '/' },
]

const contactsList = [
  { label: '@spotter_info', link: 'http://t.me/spotter_info', icon: 'contacts/icon-tg' },
  { label: 'info@spotter.ru', link: 'mailto:info@spotter.ru', icon: 'contacts/icon-mail' },
  { label: '7 800 999-99-99', link: 'tel:+78009999999', icon: 'contacts/icon-phone' },
]

const getContainerClass = computed(() => {
  switch (props.layout) {
    case 'lk':
      return 'container-lk'
    default:
      return 'container'
  }
})
</script>

<style lang="scss" scoped>
.footer {
  display: flex;
  flex-direction: column;
  background: var(--blackMain);

  &--light {
    background: #EDEEEF;
    border-top: 1px solid #D9D9E0;

    .footer {
      &__description,
      &__label {
        color: var(--grayLight);
      }

      &__icon {
        ::v-deep(.ui-icon) {
          svg > * {
            fill: var(--blackMain);
          }
        }
      }

      &__bottom {
        background: #EDEEEF;
        border-top: 1px solid #D9D9E0;
      }

      &__text {
        color: var(--grayLight);
      }
    }
  }

  &__box {
    display: grid;
    padding: 40px 0 56px;

    @include mq($bp-small) {
      // grid-template-columns: minmax(320px, 600px) 1fr;
      grid-template-columns: 1fr 1fr;
      padding: 56px 0;
    }
  }

  &__logo {
    margin-bottom: 15px;

    @include mq($bp-small) {
      margin-bottom: 20px;
    }
  }

  &__description {
    line-height: 18px;
    font-size: 13px;
    color: var(--gray);

    @include mq($bp-small) {
      line-height: 24px;
      font-size: 16px;
    }
  }

  &__cols {
    display: grid;
    grid-template-columns: repeat(2, auto);
    margin-top: 40px;

    @include mq($bp-small) {
      margin-top: 0;
    }
  }

  &__col {
    display: flex;
    align-items: flex-start;
    flex-direction: column;

    @include mq($bp-small) {
      max-width: 432px;
      margin-right: 40px;
    }
  }

  &__label {
    color: var(--gray);
    font-weight: 500;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;

    @include mq($bp-small) {
      font-size: 18px;
      line-height: 26px;
    }
  }

  &__list {
    display: flex;
    flex-direction: column;
  }

  &__item {
    margin-top: 12px;

    @include mq($bp-small) {
      margin-top: 16px;
    }

    &:first-child {
      margin-top: 16px;
    }
  }

  &__link {
    display: flex;
    align-items: center;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    white-space: nowrap;

    @include mq($bp-small) {
      font-size: 16px;
      line-height: 22px;
    }

    &:hover {
      color: var(--lime);
    }
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    margin-right: 4px;

    @include mq($bp-small) {
      margin-right: 8px;
    }
  }

  &__bottom {
    background: var(--grayDark);
  }

  &__line {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 0 24px;

    @include mq($bp-small) {
      flex-direction: row;
      justify-content: space-between;
      padding: 20px 0;
    }
  }

  &__rules {
    display: grid;
    grid-gap: 4px;
    margin-top: 4px;

    @include mq($bp-small) {
      grid-gap: 20px;
      grid-template-columns: repeat(2, auto);
      margin-top: 0;
    }
  }

  &__text {
    font-size: 12px;
    line-height: 16px;
    color: var(--gray);

    @include mq($bp-small) {
      font-size: 14px;
    }
  }
}
</style>
