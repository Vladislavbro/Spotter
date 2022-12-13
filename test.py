from models import Products, Categories, Queries
from datetime import timedelta, datetime


class Top(object):
    """
    1. В каждой категории нижнего уровня отбираются топ 50 товаров по росту
    оборота в процентах.
    Дополнительное условие:
    - Оборот товара в первом периоде должен быть больше 10 000 рублей
    2. Алгоритм вычленияет главное слово и характеристику и забивает результат
    в поиск на маркетплейсе
    Условия отбора:
    - товаров по запросу должно быть не больше 300
    3. Составляется таблица товаров из выдачи с сортировкой по обороту от
    большего к меньшему
    Условия отбора:
    - Оборот первого не меньше 500к, оборот десятого не меньше 100к
    - Количество товаров с продажами: не меньше 20%
    - Средний чек в категории месяц назад и сейчас отличается не более чем
    на +-10%
    - Оборот в категории месяц назад и сейчас отличается не более чем на +-10%
    Если все условия пройдены - то информация о нише и топ 50 товарах
    отправляются в раздел топ категории
    """
    categories = list()
    profit_first_top = 500000 / 3
    profit_ten_top = 100000 / 3
    profit_last_decada = 10000 / 3

    def __init__(self):
        super(Top, self).__init__()
        self.categories = Categories.objects(parse=True)
        self.calculate()

    def get_avg(self, values):
        if len(values):
            return sum([sum(value) / len(value) for value in values if len(value)]) / len(values)
        else:
            return 0

    def get_sum(self, values):
        return sum([sum(value) for value in values])

    def calculate(self):
        end_prev_period = (datetime.now() - timedelta(days=10)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        start_prev_period = end_prev_period - timedelta(days=10)
        for category in self.categories:
            products = Products.objects(categories__in=[category.wb_id])
            # top_products = products.filter(last_decada_profit__gte=profit_last_decada).order_by('-current_decada_sales')[0:50]
            top_products = products.order_by('-current_decada_sales')[0:50]
            queries = list()
            for top in top_products:
                features = top.features
                features.sort()
                if top.root and features and [top.root, features] not in queries:
                    query = [top.root, features]
                    queries.append(query)
            for query in queries:
                print('query', query)
                query_products = Products.objects(
                    root=query[0],
                    features__all=query[1]
                ).order_by('-current_decada_sales')
                query_products_count = query_products.count()
                query.append(query_products_count)
                if query_products_count <= 300 and query_products_count >= 10:
                    first_product_decada_profit = (
                        (query_products[0].current_decada_sales or 0)
                        *
                        (query_products[0].price or 0)
                    )
                    ten_product_decada_profit = (
                        (query_products[9].current_decada_sales or 0)
                        *
                        (query_products[9].price or 0)
                    )
                    products_with_sales = query_products.filter(
                        current_decada_sales__gt=0).count()
                    avg_price_prev_period = self.get_avg(
                        [[s.price for s in p.sizes if s.price
                          and s.date >= start_prev_period
                          and s.date < end_prev_period] for p in products]
                    )
                    avg_price_period = self.get_avg(
                        [[s.price for s in p.sizes if s.price
                          and s.date >= end_prev_period] for p in products]
                    )
                    profit_prev_period = self.get_sum(
                        [[s.profit or ((s.sales or 0) *
                                       (s.price or p.price or 0))
                          for s in p.sizes
                          if s.date >= start_prev_period
                          and s.date < end_prev_period
                          ]
                         for p in products]
                    )
                    profit_period = self.get_sum(
                        [[s.profit or ((s.sales or 0) *
                                       (s.price or p.price or 0))
                          for s in p.sizes if s.date >= end_prev_period]
                         for p in products]
                    )
                    top = {
                        'query': query,
                        'query_products_count': query_products_count,
                        'first_product_decada_profit': first_product_decada_profit,
                        'ten_product_decada_profit': ten_product_decada_profit,
                        'products_with_sales': products_with_sales,
                        'avg_price_prev_period': avg_price_prev_period,
                        'avg_price_period': avg_price_period,
                        'profit_prev_period': profit_prev_period,
                        'profit_period': profit_period,
                    }
                    print(top)
                    # Оборот первого не меньше 500к
                    if first_product_decada_profit < self.profit_first_top:
                        continue
                    # оборот десятого не меньше 100к
                    if ten_product_decada_profit < self.profit_ten_top:
                        continue
                    # Количество товаров с продажами: не меньше 20%
                    if products_with_sales / query_products_count < 1/5:
                        continue
                    # Средний чек в категории месяц назад и сейчас
                    # отличается не более чем на +-10%
                    if avg_price_period < avg_price_prev_period * 0.9:
                        continue
                    if avg_price_period > avg_price_prev_period * 1.1:
                        continue
                    # Оборот в категории месяц назад и сейчас отличается
                    # не более чем на +-10%
                    if profit_period < profit_prev_period * 0.9:
                        continue
                    if profit_period > profit_prev_period * 1.1:
                        continue
                    print('-----')
                    print('-----')
                    print('-----')
                    print('SUPERTOP')
                    print('-----')
                    print('-----')
                    print('-----')
                    print('-----')


Top()
