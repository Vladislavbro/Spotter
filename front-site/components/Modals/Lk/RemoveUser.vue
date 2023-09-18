<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="remove-user">
      <p class="remove-user__title">
        Удалить аккаунт
      </p>

      <div class="remove-user__box">
        <div class="remove-user__line">
          <span class="remove-user__label">
            Имя, фамилия:
          </span>
          {{ item.first_name }} {{ item.last_name }}
        </div>

        <div class="remove-user__line">
          <span class="remove-user__label">
            E-mail:
          </span>
          {{ item.email }}
        </div>

        <div class="remove-user__line">
          <span class="remove-user__label">
            Username:
          </span>
          {{ item.username }}
        </div>

        <!-- <div class="remove-user__line">
          <span class="remove-user__label">
            Номер телефона:
          </span>
          {{ item.phone }}
        </div> -->

        <!-- <div class="remove-user__line">
          <span class="remove-user__label">
            Пароль:
          </span>
          {{ item.password }}
        </div> -->

        <div class="remove-user__line">
          <span class="remove-user__label">
            Статус подписки:
          </span>
          {{ item.customer__subscribe_type === 'premium' ? 'Продвинутый' : item.customer__subscribe_type === 'trial' ? 'Базовый' : '--' }}
        </div>

        <div class="remove-user__line">
          <span class="remove-user__label">
            Подписка до:
          </span>
          {{ item.customer__subscribe_until || '--' }}
        </div>

        <div class="remove-user__btns">
          <UILkButton
            is-big
            full-width
            text="Удалить"
            @click="emits('success', item.id), closeModal()"
          />

          <UILkButton
            primary-gray
            is-big
            full-width
            text="Отменить"
            @click="closeModal()"
          />
        </div>
      </div>
    </div>
  </ModalsLayout>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})

const emits = defineEmits(['close', 'success'])

const closeModal = () => {
  emits('close')
}
</script>

<style lang="scss" scoped>
.remove-user {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 740px;
  padding: 40px 0 32px;
  color: var(--blackMain);
  background: #FFFFFF;
  border-radius: 16px;

  &__title {
    @include h4;

    margin-bottom: 32px;
    text-align: center;
  }

  &__box {
    width: 100%;
    max-width: 460px;
    display: grid;
    grid-gap: 20px;
  }

  &__line {
    display: flex;
    align-items: center;
    padding-bottom: 8px;
    font-size: 14px;
    line-height: 18px;
    border-bottom: 1px solid #E9E9EA;
  }

  &__label {
    margin-right: 4px;
    color: var(--grayLight);
  }

  &__btns {
    display: grid;
    grid-gap: 12px;
    grid-template-columns: repeat(2, 200px);
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
