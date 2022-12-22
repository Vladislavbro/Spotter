# import os
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from flask import Flask, request, jsonify
from models import Categories, Products, Config, Queries
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
    # config = Config.objects(queries_done=True).first()
    # queries = Queries.objects(current_parsing_id=config.current_parsing_id)
    if model == 'queries':
        items = Queries.objects(current_parsing_id=1671570010)
    elif model == 'categories':
        items = Categories.objects.all()
    items = items[((page - 1) * 100):page * 100]
    if model == 'queries':
        return {
            'items': [{
                'id': str(i.id),
                'name': i.root + ' ' + ' '.join(i.features),
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
            'items': [{
                'id': str(i.id),
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
