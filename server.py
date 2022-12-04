# import os
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from flask import Flask, request, jsonify
from models import Categories, Products
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
# import spacy
from collections import Counter

app = Flask(__name__)
# nlp = spacy.load('ru_core_news_md')


def get_children(category, categories):
    return [{
        **c,
        'children': get_children(c, categories)
    } for c in categories if c.get('parent') == category['wb_id']]


def get_top_v2():
    # Путь 2 (товары с быстрым ростом оборота):
    # 1. В каждой категории нижнего уровня отбираются топ 50 товаров по росту оборота в процентах.
    # Дополнительное условие:
    # - Оборот товара в первом периоде должен быть больше 10 000 рублей
    # 2. Алгоритм вычленияет главное слово и характеристику и забивает результат в поиск на маркетплейсе
    # Условия отбора:
    # - товаров по запросу должно быть не больше 300
    # 3. Составляется таблица товаров из выдачи с сортировкой по обороту от большего к меньшему
    # Условия отбора:
    # - Оборот первого не меньше 500к, оборот десятого не меньше 100к
    # - Количество товаров с продажами: не меньше 20%
    # - Средний чек в категории месяц назад и сейчас отличается не более чем на +-10%
    # - Оборот в категории месяц назад и сейчас отличается не более чем на +-10%
    # Если все условия пройдены - то информация о нише и топ 50 товарах отправляются в раздел ""топ категории"""
    top = list()


def get_avg(values):
    if len(values):
        return sum([sum(value) / len(value) for value in values if len(value)]) / len(values)
    else:
        return 0


def get_sum(values):
    return sum([sum(value) for value in values])


def get_top_v1():
    # Путь 1 (товары с высоким оборотом):
    # 1. В каждой категории нижнего уровня отбираются топ 50 товаров по обороту с сортировкой от большего к меньшему
    # Условия отбора:
    # - Оборот первого товара не меньше 500к, оборот десятого товара не меньше 100к
    # - Количество товаров в категории: не более 300
    # - Количество товаров с продажами: не меньше 20%
    # - Средний чек в категории месяц назад и сейчас отличается не более чем на +-10%
    # - Оборот в категории месяц назад и сейчас отличается не более чем на +-10%
    # Если все условия пройдены - то информация о нише и топ 50 товарах отправляются в раздел ""топ категории""
    # для декады делим месяц на три
    profit_first_top = 500000 / 3
    profit_ten_top = 100000 / 3
    end_prev_period = (datetime.now() - timedelta(days=10)).replace(
        hour=0, minute=0, second=0, microsecond=0)
    start_prev_period = end_prev_period - timedelta(days=10)
    top = list()
    for category in Categories.objects(parse=True).all():
        products = Products.objects(categories__in=[category.wb_id])
        _count = products.count()
        # print(category.name, _count)
        if _count <= 300 and _count > 10:
            top_products = products.order_by('-current_decada_sales')[0:50]
            products_with_sales = products.filter(current_decada_sales__gt=0).count()
            profit_period = get_sum([[s.profit or ((s.sales or 0) * (s.price or p.price or 0)) for s in p.sizes if s.date >= end_prev_period] for p in products])

            sellers = len(list(set([p.brand_id for p in products])))
            sellers_with_sales = len(list(set([p.brand_id for p in products.filter(current_decada_sales__gt=0)])))
            # .filter(current_decada_sales__gt=0)
            # profit_prev_period = get_avg([[s.price for s in p.sizes if s.price and s.date >= start_prev_period and s.date < end_prev_period] for p in products])
            avg_price_prev_period = get_avg([[s.price for s in p.sizes if s.price and s.date >= start_prev_period and s.date < end_prev_period] for p in products])
            avg_price_period = get_avg([[s.price for s in p.sizes if s.price and s.date >= end_prev_period] for p in products])
            sales_period = get_sum([[(s.sales or 0) for s in p.sizes if s.date >= end_prev_period] for p in products])
            top_category = {
                '_id': {
                    '$oid': str(category.id)
                },
                'wb_id': category.wb_id,
                'name': category.name,
                'url': category.url,
                'profit_period': profit_period,
                'first_product_price': top_products[0].price,
                'first_product_decada_sales': top_products[0].current_decada_sales,
                'first_product_decada_profit': (
                    (top_products[0].current_decada_sales or 0)
                    *
                    (top_products[0].price or 0)
                ),
                'ten_product_price': top_products[10].price,
                'ten_product_decada_sales': top_products[10].current_decada_sales,
                'ten_product_decada_profit': (
                    (top_products[10].current_decada_sales or 0)
                    *
                    (top_products[10].price or 0)
                ),
                'products_count': _count,
                'products_with_sales': products_with_sales,
                'sales_period': sales_period,
                'sellers': sellers,
                'sellers_with_sales': sellers_with_sales,
                'rel_sellers': sellers_with_sales / sellers,
                'rel_sales': products_with_sales / _count,
                'avg_price_prev_period': avg_price_prev_period,
                'avg_price_period': avg_price_period,
            }
            print(top_category)
            if (
                    top_category['first_product_decada_profit'] >= profit_first_top and
                    top_category['ten_product_decada_profit'] >= profit_ten_top and
                    top_category['rel_sales'] >= 1/5 and
                    top_category['avg_price_prev_period'] > 0 and
                    top_category['avg_price_period'] > 0 and
                    top_category['avg_price_period'] >= top_category['avg_price_prev_period'] * 0.9 and
                    top_category['avg_price_period'] <= top_category['avg_price_prev_period'] * 1.1):
                top_category['top'] = True
            top.append(top_category)
    return {
        'top': top
    }


@app.route('/api/categories')
def categories_list():
    out = []
    categories = json.loads(Categories.objects().all().to_json())
    for root in [c for c in categories if c.get('parent') is None]:
        root['children'] = get_children(root, categories)
        out.append(root)
    return {
        'categories': out
    }


@app.route('/api/categories-top')
def categories_top():
    # for category in Categories.objects(parse=True):
    #     print(f'{category.name}|https://www.wildberries.ru{category.url}|{category.shard}|{category.query}|{Products.objects(categories__in=[category.wb_id]).count()}')
    # parent_ids = list(set([c.parent for c in Categories.objects.all()]))
    # categories = Categories.objects(wb_id__nin=parent_ids).to_json()
    return get_top_v1()


def get_category_stat(category):
    pass


def get_child_ids(category, ids):
    for child in Categories.objects(parent=category.wb_id):
        ids.append(child.wb_id)
        get_child_ids(child, ids)
    return ids


@app.route('/api/categories/<id>')
def category(id):
    root_category = Categories.objects.get(pk=id)
    ids = get_child_ids(root_category, [root_category.wb_id])
    products = Products.objects(category_wb_id__in=ids)
    counter = Counter([p.root for p in products.filter(root__ne=None).only('root')])
    groups = sorted(counter.items(), key=lambda item: item[1], reverse=True)
    groups = [[g[0], g[1]] for g in groups if g[1] > 15]
    for group in groups:
        current_decada_sales = products.filter(root=group[0]).sum('current_decada_sales')
        last_decada_sales = products.filter(root=group[0]).sum('last_decada_sales')
        growth = int(current_decada_sales / last_decada_sales * 100)
        group += [last_decada_sales, current_decada_sales, growth]
    return {
        'category': json.loads(root_category.to_json()),
        'ids': ids,
        'info': products.count(),
        'groups': groups
    }


@app.route('/api/data')
def data():
    return {
        'products': json.loads(Products.objects.filter(to_sort=True, inner_rating__gt=0).order_by('-inner_rating').limit(30).to_json()),
        'totalPages': int(Products.objects.filter(to_sort=True, inner_rating__gt=0).count() / 30),
        'categories': json.loads(Categories.objects.to_json()),
    }


@app.route('/api/products')
def products():
    page = int(request.args.get('page'))
    skip = (page - 1) * 30
    products = Products.objects.filter(to_sort=True, inner_rating__gt=0).order_by('-inner_rating').skip(skip).limit(30)
    return {
        'products': json.loads(products.to_json()),
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
