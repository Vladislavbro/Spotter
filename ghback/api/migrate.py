import requests
# from api.mongo_models import Categories, Products, Config, Queries
# from api.mongo_models import Config as Configs
from api.models import Category, Product, Config, Query
from time import sleep
from datetime import datetime, timedelta
import time
import sys
import re
import json
from telegram import Bot
import sys, traceback
from json import JSONDecodeError
from random import choice
import os
from urllib import request

TOKEN = '507933514:AAHP_BHtTUEES3Mq9giC231W4ZkvfeqSBb0'
bot = Bot(token=TOKEN)


class Migrate(object):

    def __init__(self):
        super(Migrate, self).__init__()
        # config -> Config
        # categories -> Category
        # queries -> Query
        # products -> Product & Sale

    def create_config(self, data):
        data = json.loads(data)
        config = Config.objects.create(
            mongo_id=data['_id']['$oid'],
            thread_id=0,
            parsing_date=data.get('current_parsing_date', {}).get('$date'),
            current_parsing_id=data.get('current_parsing_id'),
            parsing_done=data.get('parsing_done', False),
            queries_done=data.get('queries_done', False),
            queries_calculated=data.get('queries_calculated', False),
            categories_calculated=data.get('categories_calculated', False),
            products_calculated=data.get('products_calculated', False),
            calculated=data.get('calculated', False),
        )
        return config.id

    def create_category(self, data):
        data = json.loads(data)
        category = Category.objects.create(
            mongo_id=data['_id']['$oid'],
            name=data['name'],
            wb_id=data['wb_id'],
            parent=data.get('parent'),
            seo=data.get('seo'),
            shard=data.get('shard'),
            wb_query=data.get('query'),
            url=data['url'],
            parse=data['parse'],
            parsed_at=datetime.utcfromtimestamp(int(data.get(
                'parsed_at', {}).get('$date')) / 1000) if data.get('parsed_at') else None,
            last_parsed_page_at=datetime.utcfromtimestamp(int(data.get(
                'last_parsed_page_at', {}).get('$date')) / 1000) if data.get('last_parsed_page_at') else None,
            last_parsed_page=data.get('last_parsed_page'),
            start_parsing_at=datetime.utcfromtimestamp(int(data.get(
                'start_parsing_at', {}).get('$date')) / 1000) if data.get('start_parsing_at') else None,
            current_parsing_id=data.get('current_parsing_id'),
            updated_at=datetime.utcfromtimestamp(int(data.get(
                'updated_at', {}).get('$date')) / 1000) if data.get('updated_at') else None,
            profit_period=data.get('profit_period'),
            profit_prev_period=data.get('profit_prev_period'),
            sales_period=data.get('sales_period'),
            avg_price_prev_period=data.get('avg_price_prev_period'),
            avg_price_period=data.get('avg_price_period'),
            first_product_price=data.get('first_product_price'),
            ten_product_price=data.get('ten_product_price'),
            products_count=data.get('products_count'),
            products_with_sales=data.get('products_with_sales'),
            sellers=data.get('sellers'),
            sellers_with_sales=data.get('sellers_with_sales'),
            rel_sellers=data.get('rel_sellers'),
            rel_sales=data.get('rel_sales'),
            top=data.get('top'),
            ten_product_profit_top=data.get('ten_product_profit_top'),
            first_product_profit_top=data.get('first_product_profit_top'),
            profit_top=data.get('profit_top'),
            avg_price_top=data.get('avg_price_top'),
            rel_sales_top=data.get('rel_sales_top'),
            calculated=data.get('calculated'),
            products_calculated=data.get('products_calculated'),
        )
        return category.id

    def create_query(self, data):
        data = json.loads(data)
        print('create_query', data)
        category = Category.objects.get(mongo_id=data['category_id']['$oid'])
        query = Query.objects.create(
            category=category,
            mongo_id=data['_id']['$oid'],
            mongo_category_id=data['category_id']['$oid'],
            articuls=data.get('articuls'),
            root=data.get('root'),
            features=data.get('features'),
            products_count=data.get('products_count'),
            products_with_sales=data.get('products_with_sales'),
            rel_products_with_sales=data.get('rel_products_with_sales'),
            first_product_hom_profit=data.get('first_product_hom_profit'),
            ten_product_hom_profit=data.get('ten_product_hom_profit'),
            avg_price_prev_period=data.get('avg_price_prev_period'),
            avg_price_period=data.get('avg_price_period'),
            profit_prev_period=data.get('profit_prev_period'),
            profit_period=data.get('profit_period'),
            sales_period=data.get('sales_period'),
            sellers=data.get('sellers'),
            sellers_with_sales=data.get('sellers_with_sales'),
            parsed_at=datetime.utcfromtimestamp(int(data.get(
                'parsed_at', {}).get('$date')) / 1000) if data.get('parsed_at') else None,
            last_parsed_page=data.get('last_parsed_page'),
            current_parsing_id=data.get('current_parsing_id'),
            calculated=data.get('calculated'),
            top=data.get('top'),
            ten_product_profit_top=data.get('ten_product_profit_top'),
            first_product_profit_top=data.get('first_product_profit_top'),
            products_with_sales_top=data.get('products_with_sales_top'),
            profit_top=data.get('profit_top'),
            avg_price_top=data.get('avg_price_top'),
            rel_sales_top=data.get('rel_sales_top'),
        )
        return query.id

    def create_product(self, data):
        data = json.loads(data)
        print('create_product', data['name'])
        product = Product.objects.create(
            articul=data.get('articul'),
            name=data.get('name'),
            root=data.get('root'),
            entity=data.get('entity'),
            features=data.get('features'),
            brand=data.get('brand'),
            brand_id=data.get('brand_id'),
            queries=data.get('queries'),
            categories=data.get('categories'),
            subject_id=data.get('subject_id'),
            rating=data.get('rating'),
            feedbacks=data.get('feedbacks'),
            is_new=data.get('is_new'),
            price=data.get('price'),
            priceU=data.get('priceU'),
            quantity=data.get('quantity'),
            sales=data.get('sales'),
            created_at=datetime.utcfromtimestamp(int(data.get(
                'created_at', {}).get('$date')) / 1000) if data.get('created_at') else None,
            updated_at=datetime.utcfromtimestamp(int(data.get(
                'updated_at', {}).get('$date')) / 1000) if data.get('updated_at') else None,
            last_parsing_id=data.get('last_parsing_id'),
            parsed_at=datetime.utcfromtimestamp(int(data.get(
                'parsed_at', {}).get('$date')) / 1000) if data.get('parsed_at') else None,
            current_hom_sales=data.get('current_hom_sales'),
            last_hom_sales=data.get('last_hom_sales'),
            hom_sales_growth=data.get('hom_sales_growth'),
            current_hom_profit=data.get('current_hom_profit'),
            last_hom_profit=data.get('last_hom_profit'),
            hom_profit_growth=data.get('hom_profit_growth'),
        )

        for sale in data.get('sizes', []):
            product.sale_set.create(
                quantity=sale.get('quantity'),
                sales=sale.get('sales'),
                profit=sale.get('profit'),
                price=sale.get('price'),
                date=datetime.utcfromtimestamp(int(sale.get(
                    'date', {}).get('$date')) / 1000) if sale.get(
                        'date') else None,
            )

        # sizes = EmbeddedDocumentListField('Sizes')

        return product.id
