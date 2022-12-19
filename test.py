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
    category = None
    profit_first_top = 500000 / 3
    profit_ten_top = 100000 / 3
    profit_last_decada = 10000 / 3
    end_prev_period = None
    start_prev_period = None

    def __init__(self):
        super(Top, self).__init__()
        Queries.objects.delete()
        self.create_empy_file('out.csv')
        self.create_empy_file('top.csv')
        self.end_prev_period = (datetime.now() - timedelta(days=10)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.start_prev_period = self.end_prev_period - timedelta(days=10)
        self.categories = Categories.objects(parse=True)
        self.calculate_queries()
        self.calculate_categories()

    def get_avg(self, values):
        if len(values):
            return sum([sum(value) / len(value) for value in values if len(value)]) / len(values)
        else:
            return 0

    def get_sum(self, values):
        return sum([sum(value) for value in values])

    def calculate_queries(self):
        for category in self.categories:
            self.category = category
            products = Products.objects(categories__in=[self.category.wb_id])
            # top_products = products.filter(last_decada_profit__gte=profit_last_decada).order_by('-current_decada_sales')[0:50]
            top_products = products.filter(
                current_decada_sales__gt=0).order_by('-current_decada_sales')[0:50]
            for top in top_products:
                features = top.features
                features.sort()
                q = Queries.objects(root=top.root, features=features).first()
                if q is None:
                    q = Queries(root=top.root, features=features)
                    q.save()

    def calculate_categories(self):
        for category in self.categories:
            self.category = category
            products = Products.objects(categories__in=[self.category.wb_id])
            self.calculate(products)

    def create_empy_file(self, file_path):
        file_object = open(file_path, 'w')
        file_object.write(
            'root;features;query_products_count;first_product_decada_profit;' +
            'ten_product_decada_profit;products_with_sales;' +
            'avg_price_prev_period;avg_price_period;profit_prev_period;' +
            'profit_period;sellers;sellers_with_sales;sales_period\n'
        )
        file_object.close()

    def add_record(self, top, file_path):
        file_object = open(file_path, 'a')
        file_object.write(
            top.root + ';' + ','.join(top.features) + ';' +
            str(top.query_products_count) + ';' +
            str(top.first_product_decada_profit) + ';' +
            str(top.ten_product_decada_profit) + ';' +
            str(top.products_with_sales) + ';' +
            str(top.avg_price_prev_period) + ';' +
            str(top.avg_price_period) + ';' +
            str(top.profit_prev_period) + ';' +
            str(top.profit_period) + ';' +
            str(top.sellers) + ';' +
            str(top.sellers_with_sales) + ';' +
            str(top.sales_period) + '\n'
        )
        file_object.close()

    def calculate(self, query_products, query=None):
        query_products_count = query_products.count()
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
                  and s.date >= self.start_prev_period
                  and s.date < self.end_prev_period] for p in query_products]
            )
            avg_price_period = self.get_avg(
                [[s.price for s in p.sizes if s.price
                  and s.date >= self.end_prev_period] for p in query_products]
            )
            profit_prev_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes
                  if s.date >= self.start_prev_period
                  and s.date < self.end_prev_period
                  ]
                 for p in query_products]
            )
            profit_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes if s.date >= self.end_prev_period]
                 for p in query_products]
            )
            sellers = len(list(set([p.brand_id for p in query_products])))
            sellers_with_sales = len(list(set(
                [p.brand_id for p
                 in query_products.filter(current_decada_sales__gt=0)]
            )))
            sales_period = self.get_sum(
                [[(s.sales or 0) for s in p.sizes
                  if s.date >= self.end_prev_period] for p in query_products])
            top = Queries(
                root=query[0],
                features=query[1],
                query_products_count=query_products_count,
                first_product_decada_profit=first_product_decada_profit,
                ten_product_decada_profit=ten_product_decada_profit,
                products_with_sales=products_with_sales,
                avg_price_prev_period=int(avg_price_prev_period),
                avg_price_period=int(avg_price_period),
                profit_prev_period=profit_prev_period,
                profit_period=profit_period,
                sellers=sellers,
                sellers_with_sales=sellers_with_sales,
                sales_period=sales_period
            )
            if query is None:
                top.category_id = self.category.id
            self.add_record(top, 'out.csv')
            calc = dict()
            # Оборот первого не меньше 500к
            if first_product_decada_profit < self.profit_first_top:
                calc['profit_first_top'] = False
            # оборот десятого не меньше 100к
            if ten_product_decada_profit < self.profit_ten_top:
                calc['profit_ten_top'] = False
            # Количество товаров с продажами: не меньше 20%
            if products_with_sales / query_products_count < 1/5:
                calc['products_with_sales'] = False
            # Средний чек в категории месяц назад и сейчас
            # отличается не более чем на +/- 10%
            if avg_price_period < avg_price_prev_period * 0.9:
                calc['avg_price_diff'] = False
            if avg_price_period > avg_price_prev_period * 1.1:
                calc['avg_price_diff'] = False
            # Оборот в категории месяц назад и сейчас отличается
            # не более чем на +/- 10%
            if profit_period < profit_prev_period * 0.9:
                calc['profit_period'] = False
            if profit_period > profit_prev_period * 1.1:
                calc['profit_period'] = False
            top.save()
            self.add_record(top, 'top.csv')


Top()
