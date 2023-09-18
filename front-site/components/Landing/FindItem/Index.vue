<template>
  <div class="find-item">
    <div class="container">
      <div class="find-item__box">
        <h2 class="find-item__title">
          Найти прибыльный товар – <span class="find-item__title-block">просто</span>
        </h2>

        <p class="find-item__text">
          Мы создали сервис, где вы можете легко найти прибыльные товары и&nbsp;оценить риски.
        </p>

        <div class="find-item__tags">
          <p
            v-for="(item, i) in tags"
            :key="i"
            class="find-item__tag tag"
          >
            <span class="tag__icon">
              <UIBaseIcon :name="item.icon" />
            </span>
            {{ item.title }}
          </p>
        </div>

        <div class="find-item__about">
          <LandingFindItemVideo class="find-item__video" />

          <LandingFindItemAbout />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const tags = [
  {
    icon: 'landing/icon-estimate',
    title: 'Оценка ниш',
  },
  {
    icon: 'landing/icon-loop',
    title: 'Поиск прибыльного товара',
  },
  {
    icon: 'landing/icon-trands',
    title: 'Поиск трендов',
  },
  {
    icon: 'landing/icon-graphic',
    title: 'Анализ конкурентов',
  },
]
</script>

<style lang="scss" scoped>
.find-item {
  color: var(--blackMain);
  background: #F3F4F5;

  &__box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 0;

    @include mq($bp-medium) {
      padding: 100px 0;
    }
  }

  &__title {
    @include h2;

    margin-bottom: 8px;
    text-align: center;
  }

  &__title-block {
    position: relative;
    display: inline-block;
    width: 108px;
    height: 32px;
    line-height: 28px;
    color: var(--white);
    background: var(--blackMain);
    border-radius: 60px;

    @include mq($bp-small) {
      width: 170px;
      height: 48px;
      line-height: 40px;
    }
  }

  &__text {
    max-width: 600px;
    margin: 0 auto 16px;
    font-size: 13px;
    line-height: 18px;
    color: var(--grayBlack);
    text-align: center;

    @include mq($bp-small) {
      font-size: 18px;
      line-height: 26px;
      margin: 0 auto 24px;
    }
  }

  &__tags {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    grid-gap: 4px 2px;
    margin: 0 auto 28px;

    @include mq($bp-small) {
      grid-gap: 8px;
      margin: 0 auto 32px;
    }
  }

  &__about {
    width: 100%;
    display: grid;
    grid-gap: 12px;

    @include mq($bp-medium) {
      grid-gap: 16px;
      grid-template-columns: minmax(550px, 1fr) minmax(390px, 524px);
    }
  }
}

.tag {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  font-weight: 500;
  font-size: 12px;
  line-height: 16px;
  border-radius: 60px;
  background: var(--limeLighter);

  @include mq($bp-small) {
    padding: 12px 24px;
    font-size: 15px;
    line-height: 22px;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    margin-right: 4px;

    @include mq($bp-small) {
      width: 20px;
      height: 20px;
      margin-right: 8px;
    }

    ::v-deep(.ui-icon) {
      width: 100%;
    }
  }
}
</style>
