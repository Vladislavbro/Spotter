<template>
  <div class="find-item-about">
    <div class="find-item-about__body">
      <p class="find-item-about__title">
        Немного о <span>Spotter</span>
      </p>
      <p class="find-item-about__text">
        Я тоже селлер, и я регулярно покупал неликвидный товар. Из-за этого я терял деньги, время и надежду на светлое будущее.
        <br>
        <br>
        Этот сервис создан для того, чтобы отбирать востребованные товары и находить свободные ниши автоматически.
        <br>
        <br>
        Spotter уже помогает мне зарабатывать как продавцу, и я уверен, поможет и вам.
      </p>
    </div>

    <div class="find-item-about__footer">
      <div class="find-item-about__avatar">
        <img src="@/assets/images/landing/find-item/user.jpg" alt="">
      </div>

      <div class="find-item-about__user">
        <p class="find-item-about__name">
          Владислав Паламарчук
        </p>
        <p class="find-item-about__desc">
          Основатель Spotter. Вы можете связаться со&nbsp;мной напрямую.
          <a href="#" class="find-item-about__link">
            Перейти к контактам
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.find-item-about {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 24px 24px;
  background: var(--white);
  border-radius: 8px;

  @include mq($bp-small) {
    padding: 28px 40px;
    border-radius: 20px;
  }

  &__body {
    display: flex;
    flex-direction: column;
  }

  &__title {
    margin-bottom: 8px;
    font-weight: 600;
    font-size: 22px;
    line-height: 26px;

    @include mq($bp-small) {
      margin-bottom: 16px;
      font-size: 32px;
      line-height: 38px;
    }

    span {
      color: #90D80A;
    }
  }

  &__text {
    @include text_normal;
  }

  &__footer {
    display: flex;
    align-items: center;
    margin-top: 32px;

    @include mq($bp-small) {
      margin-top: 58px;
    }
  }

  &__avatar {
    flex: 0 0 auto;
    width: 64px;
    height: 64px;
    margin-right: 8px;
    border-radius: 50%;
    overflow: hidden;

    @include mq($bp-small) {
      width: 80px;
      height: 80px;
      margin-right: 16px;
    }
  }

  &__user {
    display: flex;
    flex-direction: column;
  }

  &__name {
    margin-bottom: 4px;
    font-weight: 600;
    font-size: 15px;
    line-height: 20px;

    @include mq($bp-small) {
      font-size: 18px;
      line-height: 26px;
    }
  }

  &__desc {
    color: var(--gray);
    font-size: 13px;
    line-height: 18px;

    @include mq($bp-small) {
      font-size: 15px;
      line-height: 22px;
    }
  }

  &__link {
    color: var(--blackMain);
    text-decoration: underline;
  }
}
</style>
