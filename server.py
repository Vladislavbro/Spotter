from flask import Flask, request, jsonify
from models import Categories, Products
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)


def get_children(category, categories):
    return [{
        **c,
        'children': get_children(c, categories)
    } for c in categories if c.get('parent') == category['wb_id']]


@app.route('/api/categories')
def categories():
    out = []
    categories = json.loads(Categories.objects().all().to_json())
    for root in [c for c in categories if c.get('parent') is None]:
        root['children'] = get_children(root, categories)
        out.append(root)
    return {
        'categories': out
    }


@app.route('/api/categories/<id>')
def delete_category(id):
    return {
        'category': Categories.objects.get(pk=id).to_json()
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
