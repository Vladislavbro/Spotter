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
    # config = Config.objects(queries_done=True).first()
    # queries = Queries.objects(current_parsing_id=config.current_parsing_id)
    queries = Queries.objects(current_parsing_id=1671570010)
    categories = Categories.objects.all()
    return {
        'queries': json.loads(queries.to_json()),
        'categories': json.loads(categories.to_json()),
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
