from models import Products, Categories
from datetime import timedelta, datetime


class Statistic(object):
    """docstring for Statistic."""

    def __init__(self):
        super(Statistic, self).__init__()
        self.calculate()

    def calculate(self):
        while True:
            now = datetime.utcnow()
            current_decada_start = (now - timedelta(days=10)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            last_decada_start = current_decada_start - timedelta(days=10)
            product = Products.objects(decada_sales_growth=None).first()
            if product:
                if len(product.sizes):
                    last_decada_data = [sales for sales in product.sizes
                                        if sales.date > last_decada_start
                                        and sales.date < current_decada_start]
                    product.last_decada_sales = sum([(s.sales or 0) for s
                                                     in last_decada_data])
                    current_decada_data = [sales for sales in product.sizes
                                           if sales.date > current_decada_start]
                    product.current_decada_sales = sum([(s.sales or 0) for s
                                                        in current_decada_data])
                    product.decada_sales_growth = int(
                        product.current_decada_sales /
                        product.last_decada_sales * 100)
                else:
                    product.last_decada_sales = 0
                    product.current_decada_sales = 0
                    product.decada_sales_growth = 0
                print(product.last_decada_sales, product.current_decada_sales,
                      product.decada_sales_growth)
                product.save()
            else:
                break


Statistic()
