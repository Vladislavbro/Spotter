from models import Products, Categories, Queries
from datetime import timedelta, datetime


class Top(object):
    """docstring for Statistic."""
    categories = list()
    profit_first_top = 500000 / 3
    profit_ten_top = 100000 / 3
    profit_last_decada = 10000 / 3

    def __init__(self):
        super(Top, self).__init__()
        self.categories = Categories.objects(parse=True)
        self.calculate()

    def calculate(self):
        for category in self.categories:
            products = Products.objects(categories__in=[category.wb_id])
            # top_products = products.filter(last_decada_profit__gte=profit_last_decada).order_by('-current_decada_sales')[0:50]
            top_products = products.order_by('-current_decada_sales')[0:50]
            queries = list()
            for top in top_products:
                features = top.features
                features.sort()
                print(top.root, features)
                if top.root and [top.root, features] not in queries:
                    queries.append([top.root, features])
            print(queries)


Top()
