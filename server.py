# import os
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from flask import Flask, request, jsonify, Response
from models import Categories, Products, Config, Queries
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
# import spacy
from collections import Counter
import csv

app = Flask(__name__)
# nlp = spacy.load('ru_core_news_md')


def get_children(category, categories):
    return [{
        **c,
        'children': get_children(c, categories)
    } for c in categories if c.get('parent') == category['wb_id']]


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


@app.route('/api/top')
def categories_top():
    model = request.args.get('model')
    page = int(request.args.get('page'))
    sort = request.args.get('sort')
    config = Config.objects(calculated=True).first()
    # config = Config.objects.first()
    # queries = Queries.objects(current_parsing_id=config.current_parsing_id)
    if model == 'queries':
        items = Queries.objects(
            # current_parsing_id=config.current_parsing_id,
            current_parsing_id=1672043096,
            root__ne=None
        )
    elif model == 'categories':
        items = Categories.objects(parse=True).all()
    total = items.count()
    if sort:
        items = items.order_by(f'-{sort}')
    items = items[((page - 1) * 100):page * 100]
    if model == 'queries':
        return {
            'total': total,
            'items': [{
                'id': str(i.id),
                'name': i.root + ' ' + ' '.join(i.features),
                'root': i.root,
                'features': ' '.join(i.features),
                'products_count': i.products_count,
                'first_product_decada_profit': i.first_product_decada_profit,
                'ten_product_decada_profit': i.ten_product_decada_profit,
                'products_with_sales': i.products_with_sales,
                'avg_price_prev_period': i.avg_price_prev_period,
                'avg_price_period': i.avg_price_period,
                'profit_prev_period': i.profit_prev_period,
                'profit_period': i.profit_period,
                'sellers': i.sellers,
                'sellers_with_sales': i.sellers_with_sales,
                'sales_period': i.sales_period,
                'last_parsed_page': i.last_parsed_page,
                'current_parsing_id': i.current_parsing_id,
                'top': i.top,
                'ten_product_profit_top': i.ten_product_profit_top,
                'first_product_profit_top': i.first_product_profit_top,
                'products_with_sales_top': i.products_with_sales_top,
                'profit_top': i.profit_top,
                'avg_price_top': i.avg_price_top,
                'rel_sales_top': i.rel_sales_top,
            } for i in items]
        }
    elif model == 'categories':
        return {
            'total': total,
            'items': [{
                'id': str(i.id),
                'url': i.url,
                'name': i.name,
                'profit_period': i.profit_period,
                'profit_prev_period': i.profit_prev_period,
                'first_product_price': i.first_product_price,
                'first_product_decada_sales': i.first_product_decada_sales,
                'first_product_decada_profit': i.first_product_decada_profit,
                'ten_product_price': i.ten_product_price,
                'ten_product_decada_sales': i.ten_product_decada_sales,
                'ten_product_decada_profit': i.ten_product_decada_profit,
                'products_count': i.products_count,
                'products_with_sales': i.products_with_sales,
                'sales_period': i.sales_period,
                'sellers': i.sellers,
                'sellers_with_sales': i.sellers_with_sales,
                'rel_sellers': i.rel_sellers,
                'rel_sales': i.rel_sales,
                'avg_price_prev_period': i.avg_price_prev_period,
                'avg_price_period': i.avg_price_period,
                'top': i.top,
                'ten_product_profit_top': i.ten_product_profit_top,
                'first_product_profit_top': i.first_product_profit_top,
                'profit_top': i.profit_top,
                'avg_price_top': i.avg_price_top,
                'rel_sales_top': i.rel_sales_top,
            } for i in items],
        }


@app.route('/api/export/queries')
def export_queries():
    config = Config.objects(calculated=True).first()
    items = Queries.objects(
        # current_parsing_id=config.current_parsing_id,
        current_parsing_id=1672043096,
        root__ne=None
    )

    # - Корень
    # - Характеристика
    # - Количество товаров
    # - Товары с продажами
    # - Товары с продажами (в процентах, округление до целых)
    # - Оборот первого товара
    # - Оборот десятого товара
    # - Средняя цена пред
    # - Средняя цена тек
    # - Изм средней цены (в процентах, округление до целых)
    # - Оборот пред
    # - Оброт тек
    # - Изменение оборота (в процентах, округление до целых)
    # - Количество продавцов
    # - Продавцы с продажами
    # - Продавцы с продажами (в процентах, округление до целых)
    # - Топ
    # - Топ товар 1
    # - Топ товар 10
    # - Топ товары с продажами
    # - Топ средний чек
    # - Топ оборот

    fields = ['Корень', 'Характеристики', 'Кол-во товаров',
              'Товары с продажами', 'Товары с продажами',
              'Оборот первого товара', 'Оборот десятого товара',
              'Средняя цена пред', 'Средняя цена тек', 'Изменение оборота',
              'Количество продавцов', 'Продавцы с продажами',
              'Продавцы с продажами', 'Топ', 'Топ товар 1', 'Топ товар 10',
              'Топ товары с продажами', 'Топ средний чек', 'Топ оборот']
    rows = [
        [i.root, i.features, i.products_count, i.products_with_sales,
         int(i.products_with_sales * 100 / i.products_count) if i.products_count else 0,
         i.first_product_decada_profit, i.ten_product_decada_profit,
         i.avg_price_prev_period, i.avg_price_period,
         int(i.avg_price_period * 100 / i.avg_price_prev_period),
         i.sellers, i.sellers_with_sales,
         int(i.sellers_with_sales * 100 / i.sellers),
         i.top, i.first_product_profit_top, i.ten_product_profit_top,
         i.products_with_sales_top, i.avg_price_top, i.profit_top]
        for i in items
    ]
    filename = f'{config.current_parsing_id}-queries.csv'
    file_path = f'export/{filename}'
    with open(file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    f = open(file_path, 'r')
    content = f.read()
    return Response(
        content,
        mimetype="text/csv",
        headers={
            "Content-disposition":
            f"attachment; filename={filename}"})


@app.route('/api/export/categories')
def export_categories():
    config = Config.objects(calculated=True).first()
    items = Categories.objects(parse=True).all()
    # fields = ['name', 'profit_period', 'profit_prev_period',
    #           'first_product_price', 'first_product_decada_sales',
    #           'first_product_decada_profit', 'ten_product_price',
    #           'ten_product_decada_sales', 'ten_product_decada_profit',
    #           'products_count', 'products_with_sales', 'sales_period',
    #           'sellers', 'sellers_with_sales', 'rel_sellers', 'rel_sales',
    #           'avg_price_prev_period', 'avg_price_period', 'top',
    #           'ten_product_profit_top', 'first_product_profit_top',
    #           'profit_top', 'avg_price_top', 'rel_sales_top']
    # rows = [
    #     [i.name, i.profit_period, i.profit_prev_period, i.first_product_price,
    #      i.first_product_decada_sales, i.first_product_decada_profit,
    #      i.ten_product_price, i.ten_product_decada_sales,
    #      i.ten_product_decada_profit, i.products_count, i.products_with_sales,
    #      i.sales_period, i.sellers, i.sellers_with_sales, i.rel_sellers,
    #      i.rel_sales, i.avg_price_prev_period, i.avg_price_period, i.top,
    #      i.ten_product_profit_top, i.first_product_profit_top, i.profit_top,
    #      i.avg_price_top, i.rel_sales_top] for i in items]
    fields = ['Наименование', 'Кол-во товаров',
              'Товары с продажами', 'Товары с продажами',
              'Оборот первого товара', 'Оборот десятого товара',
              'Средняя цена пред', 'Средняя цена тек', 'Изменение оборота',
              'Количество продавцов', 'Продавцы с продажами',
              'Продавцы с продажами', 'Топ', 'Топ товар 1', 'Топ товар 10',
              'Топ товары с продажами', 'Топ средний чек', 'Топ оборот']
    rows = [
        [i.name, i.products_count, i.products_with_sales,
         int(i.products_with_sales * 100 / i.products_count) if i.products_count else 0,
         i.first_product_decada_profit, i.ten_product_decada_profit,
         i.avg_price_prev_period, i.avg_price_period,
         int(i.avg_price_period * 100 / i.avg_price_prev_period),
         i.sellers, i.sellers_with_sales,
         int(i.sellers_with_sales * 100 / i.sellers),
         i.top, i.first_product_profit_top, i.ten_product_profit_top,
         i.products_with_sales_top, i.avg_price_top, i.profit_top]
        for i in items
    ]
    filename = f'{config.current_parsing_id}-categories.csv'
    file_path = f'export/{filename}'
    with open(file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    f = open(file_path, 'r')
    content = f.read()
    return Response(
        content,
        mimetype="text/csv",
        headers={
            "Content-disposition":
            f"attachment; filename={filename}"})


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
