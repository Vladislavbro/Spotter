<template>
  <div class="seller-items">
    <div class="seller-items__info">
      <LkTableTypes />

      <LkTableDate />
    </div>

    <LkTableFilter class="seller-items__filter">
      <UILkFilter
        label="Рейтинг"
      />
      <UILkFilter
        label="Оборот"
      />
      <UILkFilter
        label="Продажи, шт"
      />
    </LkTableFilter>

    <div class="seller-items__card">
      <div class="seller-items__card-header">
        <div class="seller-items__card-side">
          <LkTableSettings
            :array="headColumns"
          />

          <LkTableSort
            :array="headColumns"
          />
        </div>

        <LkTableImport />
      </div>

      <LkTable
        :head-columns="headColumns"
        class="seller-items__table seller-items-table"
      >
        <tbody>
          <tr
            v-for="(item, i) in bodyColumns"
            :key="i"
          >
            <td>
              <div class="seller-items-table-item">
                <div class="seller-items-table-item__image">
                  <img
                    src="@/assets/images/lk/item-niche-items-test.jpg"
                    alt=""
                  >
                </div>
                <div class="seller-items-table-item__info">
                  <NuxtLink
                    to="/lk/item/1"
                    class="seller-items-table-item__name"
                  >
                    <span class="seller-items-table-item__name-box">
                      {{ item.name }}
                    </span>
                    <UIBaseIcon name="lk/icon-share" />
                  </NuxtLink>
                  <a
                    href="#"
                    class="seller-items-table-item__article"
                    @click.prevent="copyText(item.article)"
                  >
                    <UIBaseIcon name="lk/icon-wb" />
                    <span>
                      Артикул:
                    </span>
                    {{ item.article }}
                    <UIBaseIcon name="lk/icon-copy" />
                  </a>
                  <p class="seller-items-table-item__rating">
                    <UIBaseIcon name="lk/icon-star" />
                    {{ item.rating }}
                    <span class="seller-items-table-item__reviews">
                      ({{ item.reviews }} отзывов)
                    </span>
                  </p>
                </div>
              </div>
            </td>
            <td>
              <div class="seller-items-table__price">
                <p class="seller-items-table__newprice">
                  {{ item.price }}
                  <span class="seller-items-table__price-percent">
                    {{ item.price_percent }}
                  </span>
                </p>
                <span class="seller-items-table__oldprice">
                  {{ item.price_old }}
                </span>
              </div>
            </td>
            <td>
              <NuxtLink
                to="/lk/seller/1"
                class="seller-items-table__link"
              >
                {{ item.seller }}
              </NuxtLink>
            </td>
            <td>
              <NuxtLink
                to="/lk/seller/1"
                class="seller-items-table__link"
              >
                {{ item.brand }}
              </NuxtLink>
            </td>
            <td>
              <p class="seller-items-table__stats">
                {{ item.turnover }}
                <span class="seller-items-table__stats-percent seller-items-table__stats-percent--good">
                  {{ item.turnover_percent }}
                </span>
              </p>
            </td>
            <td>
              <p class="seller-items-table__stats">
                {{ item.sales }}
                <span class="seller-items-table__stats-percent seller-items-table__stats-percent--good">
                  {{ item.sales_percent }}
                </span>
              </p>
            </td>
          </tr>
        </tbody>
      </LkTable>
    </div>

    <UILkButton
      text="Показать ещё"
      full-width
      class="seller-items__show-more"
    />
  </div>
</template>

<script setup>
import copyTextToClipboard from '@/utils/copyTextToClipboard'

const headColumns = [
  { label: 'Название товара', show: true },
  { label: 'Цена', show: true },
  { label: 'Продавец', show: true },
  { label: 'Бренд', show: true },
  { label: 'Оборот', show: true, info: 'Изменение по отношению к прошлому периоду в процентах' },
  { label: 'Продажи, шт.', show: true },
]

const bodyColumns = [
  {
    name: 'Топлёное масло ГХИ, 440 мл / без лактозы / без сахара Артикул',
    article: '80012708',
    rating: '4.9',
    reviews: '2384',
    price: '990 ₽',
    price_percent: '-70%',
    price_old: '7 100 ₽',
    seller: 'Чугунов Александр Валентинович (370701981555)',
    brand: 'Olesa Chugunova',
    turnover: '710 478 ₽',
    turnover_percent: '+2,2%',
    sales: '183 368',
    sales_percent: '+2,2%',
  },
]

const copyText = async (text) => {
  const msg = await copyTextToClipboard(text)
}
</script>

<style lang="scss" scoped>
.seller-items {
  &__info {
    display: grid;
    align-items: center;
    justify-content: flex-start;
    grid-gap: 24px;
    grid-template-columns: repeat(2, auto);
    margin-bottom: 32px;
  }

  &__filter {
    margin-bottom: 32px;
  }

  &__card {
    display: flex;
    flex-direction: column;
    margin-bottom: 40px;
    padding: 24px 20px 20px;
    background: var(--white);
    border-radius: 12px;
  }

  &__card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
  }

  &__card-side {
    display: grid;
    grid-gap: 8px;
    grid-template-columns: repeat(2, auto);
  }

  &__show-more {
    height: 48px;
    font-weight: 500;
    font-size: 14px;
    line-height: 16px;
    color: var(--blackMain);
    background: none;
    border-color: #D9D9E0;

    &:hover {
      background: none;
    }
  }
}

.seller-items-table {
  &__name {
    display: grid;
    grid-gap: 2px;
  }

  &__price {
    display: grid;
    grid-gap: 4px;
    line-height: 14px;
  }

  &__newprice {
    font-size: 15px;
    line-height: 18px;
  }

  &__price-percent {
    margin-left: 4px;
    padding: 4px 6px;
    font-size: 11px;
    color: #33976F;
    background: #F8F8F9;
    border-radius: 4px;
  }

  &__oldprice {
    font-size: 12px;
    text-decoration-line: line-through;
    color: #8B8B91;
  }

  &__link {
    color: #33976F;
  }

  &__stats {
    position: relative;

    &-percent {
      position: absolute;
      top: 100%;
      left: 0;
      font-size: 11px;
      line-height: 14px;

      &--bad {
        color: #CC2A2A;
      }

      &--good {
        color: #33976F;
      }
    }
  }
}

.seller-items-table-item {
  display: flex;
  align-items: flex-start;

  ::v-deep(.ui-icon) {
    svg {
      width: 16px;
      height: 16px;
    }
  }

  &__image {
    width: 60px;
    height: 65px;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__info {
    display: grid;
    grid-gap: 6px;
    max-width: 200px;
    margin-left: 16px;
  }

  &__name {
    display: flex;
    align-items: flex-end;
    font-size: 14px;
    line-height: 20px;

    &-box {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    ::v-deep(.ui-icon) {
      display: inline-flex;
    }
  }

  &__article {
    display: grid;
    grid-gap: 4px;
    grid-template-columns: repeat(4, auto);
    justify-content: flex-start;
    align-self: start;
    font-size: 13px;
    line-height: 16px;

    span {
      font-weight: 500;
    }
  }

  &__rating {
    display: grid;
    grid-gap: 2px;
    grid-template-columns: repeat(3, auto);
    justify-content: flex-start;
    align-items: center;
    font-weight: 500;
    font-size: 13px;
    line-height: 16px;

    ::v-deep(.ui-icon) {
      svg {
        width: 20px;
        height: 20px;
      }

      path {
        fill: #F2CF3A;
      }
    }
  }

  &__reviews {
    margin-left: 2px;
    font-weight: 400;
    font-size: 12px;
    line-height: 14px;
    color: #8B8B91;
  }
}
</style>
