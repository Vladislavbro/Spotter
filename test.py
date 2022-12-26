from models import Products, Categories, Queries
from datetime import timedelta, datetime


end_prev_period = (datetime.now() - timedelta(days=10)).replace(hour=0, minute=0, second=0, microsecond=0)
start_prev_period = end_prev_period - timedelta(days=10)
profit_first_top = 500000 / 3
profit_ten_top = 100000 / 3


def get_avg(self, values):
    if len(values):
        return sum([sum(value) / len(value) for value in values if len(value)]) / len(values)
    else:
        return 0


def get_sum(self, values):
    return sum([sum(value) for value in values])


def test_calculate_category(category):
    products = Products.objects(categories__in=[category.wb_id])
    category.products_count = products.count()
    print(category.name, category.products_count)
    if category.products_count > 10:
        top_products = products.order_by('-current_decada_sales')[0:50]
        category.products_with_sales = products.filter(
            current_decada_sales__gt=0).count()
        category.profit_period = get_sum([
            [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
             for s in p.sizes if s.date >= end_prev_period]
            for p in products])
        category.profit_prev_period = get_sum([
            [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
             for s in p.sizes if s.date >= start_prev_period and
             s.date < end_prev_period]
            for p in products])
        category.sellers = len(list(set([p.brand_id for p in products])))
        category.sellers_with_sales = len(list(set([
            p.brand_id for p
            in products.filter(current_decada_sales__gt=0)])))
        category.avg_price_prev_period = get_avg([
            [s.price for s in p.sizes
             if s.price and s.date >= start_prev_period and
             s.date < end_prev_period] for p in products])
        category.avg_price_period = get_avg([
            [s.price for s in p.sizes
             if s.price and s.date >= end_prev_period]
            for p in products])
        category.sales_period = get_sum([
            [(s.sales or 0) for s in p.sizes
             if s.date >= end_prev_period] for p in products])

        category.first_product_price = top_products[0].price
        category.first_product_decada_sales = top_products[0].current_decada_sales
        category.first_product_decada_profit = (
            (top_products[0].current_decada_sales or 0)
            *
            (top_products[0].price or 0)
        )
        category.ten_product_price = top_products[9].price
        category.ten_product_decada_sales = top_products[9].current_decada_sales
        category.ten_product_decada_profit = (
            (top_products[9].current_decada_sales or 0)
            *
            (top_products[9].price or 0)
        )
        category.rel_sellers = category.sellers_with_sales / category.sellers
        category.rel_sales = category.products_with_sales / category.products_count
        if category.first_product_decada_profit >= profit_first_top:
            category.first_product_profit_top = True
        if category.ten_product_decada_profit >= profit_ten_top:
            category.ten_product_profit_top = True
        if category.rel_sales >= 1/5:
            category.rel_sales_top = True
        if (
                category.avg_price_period >=
                category.avg_price_prev_period * 0.9 and
                category.avg_price_period <=
                category.avg_price_prev_period * 1.1):
            category.avg_price_top = True
        if (
                category.profit_period >=
                category.profit_prev_period * 0.9 and
                category.profit_period <=
                category.profit_prev_period * 1.1):
            category.profit_top = True
        if (
                category.first_product_profit_top and
                category.ten_product_profit_top and
                category.rel_sales_top and
                category.avg_price_top and
                category.profit_top):
            category.top = True
        category.calculated = True
        category.save()
        print(category.to_json())
