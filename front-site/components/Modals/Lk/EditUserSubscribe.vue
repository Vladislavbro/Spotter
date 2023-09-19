<template>
  <ModalsLayout
    @close="closeModal()"
  >
    <div class="edit-user-subscribe">
      <p class="edit-user-subscribe__title">
        Изменить тариф
      </p>

      <form
        class="edit-user-subscribe__box"
        @submit.prevent="onSubmit()"
      >
        <div class="edit-user-subscribe__line">
          <span class="edit-user-subscribe__label">
            Имя, фамилия:
          </span>
          {{ item.first_name }} {{ item.last_name }}
        </div>

        <div class="edit-user-subscribe__line">
          <span class="edit-user-subscribe__label">
            E-mail:
          </span>
          {{ item.email }}
        </div>

        <div class="edit-user-subscribe__line">
          <span class="edit-user-subscribe__label">
            Username:
          </span>
          {{ item.username }}
        </div>

        <!-- <div class="edit-user-subscribe__line">
          <span class="edit-user-subscribe__label">
            Номер телефона:
          </span>
          {{ item.phone }}
        </div> -->

        <!-- <div class="edit-user-subscribe__line">
          <span class="edit-user-subscribe__label">
            Пароль:
          </span>
          {{ item.password }}
        </div> -->

        <div class="edit-user-subscribe__status">
          <p class="edit-user-subscribe__status-label">
            Статус подписки:
          </p>
          <UILkRadio
            id="status-pro"
            v-model="form.customer__subscribe_type"
            value="premium"
            text="Продвинутый"
          />
          <UILkRadio
            id="status-base"
            v-model="form.customer__subscribe_type"
            value="trial"
            text="Базовый"
          />
        </div>

        <!-- <UIBaseInput
          v-model="form.date"
          label="Подписка до"
          placeholder="дд.мм.гггг"
        /> -->

        <UILkButton
          type="submit"
          text="Изменить"
          is-big
          full-width
          class="edit-user-subscribe__btn"
        />
      </form>
    </div>
  </ModalsLayout>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
})

const form = reactive({
  customer__subscribe_type: 'premium',
  date: '',
})

const emits = defineEmits(['close', 'success'])

const closeModal = () => {
  emits('close')
}

const onSubmit = () => {
  emits('success', {
    id: props.item.id,
    ...form,
  })
  closeModal()
}

onMounted(() => {
  if (props.item) {
    form.status = props.item.status
    form.date = props.item.date
  }
})
</script>

<style lang="scss" scoped>
.edit-user-subscribe {
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

    margin-bottom: 28px;
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

  &__status {
    display: grid;
    justify-content: flex-start;
    grid-gap: 20px;
    grid-template-columns: repeat(3, auto);
    margin: 8px 0 4px;

    &-label {
      font-weight: 500;
      font-size: 14px;
      line-height: 18px;
    }
  }

  &__btn {
    max-width: 200px;
    margin: 20px auto 0;
  }
}
</style>
