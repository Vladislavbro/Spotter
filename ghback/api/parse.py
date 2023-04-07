import requests
# from api.mongo_models import Categories, Products, Config, Queries
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
from api.proxies import proxies
from random import choice
from random_user_agent.user_agent import UserAgent
import spacy
import os
from urllib import request

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
nlp = spacy.load('ru_core_news_md')

user_agent_rotator = UserAgent()
TOKEN = '507933514:AAHP_BHtTUEES3Mq9giC231W4ZkvfeqSBb0'
bot = Bot(token=TOKEN)

sys.setrecursionlimit(10**6)


class Parser(object):
    """docstring for Parser."""
    regions = '68,64,83,4,38,80,33,70,82,86,75,30,69,1,48,22,66,31,40,71'
    dest = '-1029256,-102269,-2162196,-1257786'
    couponsGeo = '12,3,18,15,21'
    page = 1
    category = None
    query = None
    adminIds = [259180458]
    config = None
    end_prev_period = None
    start_prev_period = None
    profit_first_top = 500000 / 2
    profit_ten_top = 100000 / 2

    def __init__(self):
        super(Parser, self).__init__()
        self.config = Config.objects.first()
        self.set_period_dates()
        self.processing()

    def get_url(self, url):
        try:
            headers = {
                'User-Agent': user_agent_rotator.get_random_user_agent()
            }
            proxy = choice(proxies)
            response = requests.get(url, headers=headers, proxies={
                'http': proxy,
                'https': proxy,
            })
            return response
        except:
            print('get_url except', proxy)
            return self.get_url(url)

    def processing(self):
        if self.config.parsing_done is not True:
            self.notify('Парсинг категорий начался')
            self.get_category()
        elif self.config.queries_done is not True:
            self.notify('Парсинг запросов начался')
            self.get_query()
        elif self.config.queries_calculated is not True:
            self.notify('Расчет запросов начался')
            self.calculate_queries()
        elif self.config.categories_calculated is not True:
            self.notify('Расчет категорий начался')
            self.calculate_categories()
        elif self.config.products_calculated is not True:
            self.notify('Расчет топ товаров начался')
            self.calculate_products()
        else:
            self.config.calculated = True
            self.config.save()
            date = datetime.utcnow()
            self.config = Config(
                current_parsing_date=date,
                current_parsing_id=int(date.timestamp()),
            )
            self.config.save()
            self.notify('Новый цикл начался')
            self.get_category()

    def create_queries(self):
        categories = Category.objects.filter(parse=True)
        for category in categories:
            self.category = category
            products = Product.objects.filter(
                categories__contains=[self.category.wb_id])
            top_products = products.filter(
                last_hom_profit__gte=10000/3,
                current_hom_sales__gt=0,
            ).exclude(root=None).order_by('-current_hom_sales')[0:50]
            for top in top_products:
                features = top.features
                features.sort()
                q = Query.objects.filter(
                    root=top.root,
                    features=features,
                    current_parsing_id=self.config.current_parsing_id
                ).first()
                if q is None:
                    q = Query(
                        root=top.root,
                        features=features,
                        category_id=category.id,
                        current_parsing_id=self.config.current_parsing_id
                    )
                    q.save()
                    print(q.root, q.features)

    def update_category(self, child):
        category = Category.objects.filter(wb_id=child['id']).first()
        if category is None:
            category = Category(wb_id=child['id'])
        category.name = child.get('name')
        category.shard = child.get('shard')
        category.wb_query = child.get('query')
        category.parent = child.get('parent')
        category.seo = child.get('seo')
        category.url = child.get('url')
        category.shard = child.get('shard')
        category.parse = child.get('childs') is None
        category.save()

    def get_categories(self):
        self.upgrade_parsing()
        f = open('data/catalog.txt', 'r')
        content = f.read()
        categoryUrlList = [line for line in content.strip().split('\n')]
        # if '/catalog/' in line]
        url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
        response = self.get_url(url)
        data = response.json()
        for item in [item for item in data if item['name'] in categoryUrlList]:
            self.update_category(item)
            for child in item.get('childs', []):
                if child['url'] in categoryUrlList:
                    self.update_category(child)
                    if child.get('shard') == 'blackhole':
                        for subchild in child.get('childs', []):
                            self.update_category(subchild)

    def upgrade_parsing(self):
        Category.objects.update(
            # parse=False,
            parsed_at=None,
            last_parsed_page=None,
            last_parsed_page_at=None,
            start_parsing_at=None,
        )

    def notify(self, text):
        for id in self.adminIds:
            try:
                bot.send_message(chat_id=id, text=text)
            except:
                print('send message except')

    def get_query(self):
        self.query = Query.objects.filter(
            current_parsing_id=self.config.current_parsing_id,
            parsed_at=None,
        ).exclude(root=None).first()
        if self.query is None:
            self.notify('Парсинг запросов закончился')
            self.config.queries_done = True
            self.config.save()
            return self.processing()
        else:
            self.category = self.query.category_id
            if self.query.last_parsed_page and self.query.last_parsed_page < 5:
                self.page = self.query.last_parsed_page + 1
            else:
                self.get_query_detail()
                self.page = 1
            return self.query_crawl()

    def get_category(self):
        self.category = Category.objects.filter(parsed_at=None,
                                                parse=True).first()
        if self.category is None:
            self.notify('Парсинг категорий закончился')
            Category.objects.filter(parse=True).update(
                calculated=False,
                products_calculated=False,
                parsed_at=None,
                last_parsed_page=None,
                last_parsed_page_at=None,
                start_parsing_at=None,
            )
            self.config.parsing_done = True
            self.config.save()
            self.create_queries()
            return self.get_query()
        else:
            if self.category.last_parsed_page:
                self.page = self.category.last_parsed_page + 1
            else:
                self.category.start_parsing_at = datetime.utcnow()
                self.category.save()
                self.page = 1
            return self.crawl()

    def get_query_detail(self):
        query = self.query.root + ' ' + ' '.join(self.query.features)
        url = (
            'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&'
            f'couponsGeo={self.couponsGeo}&curr=rub&dest={self.dest}&'
            f'emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&'
            f'query={query}&reg=1&regions={self.regions}&resultset=filters&'
            'sort=popular&spp=32&sppFixGeo=4&suppressSpellcheck=false'
        )
        response = self.get_url(url)
        if response.status_code == 200 and response.text != '':
            try:
                data = json.loads(r"{}".format(response.text))
                self.query.products_count = data.get('data', {}).get('total', 0)
                self.query.save()
                print('self.query.products_count', self.query.id,
                      self.query.products_count)
            except JSONDecodeError as e:
                self.notify('get_query_detail JSONDecodeError ' + query)
                print('get_query_detail JSONDecodeError', e, url)
            except Exception as e:
                print('except', str(e))
        else:
            self.notify(f'get_query_detail {response.status_code} {query}')

    def query_crawl(self):
        query = self.query.root + ' ' + ' '.join(self.query.features)
        url = (
            'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&'
            f'couponsGeo={self.couponsGeo}&curr=rub&dest={self.dest}&'
            f'emp=0&lang=ru&locale=ru&page={self.page}&pricemarginCoeff=1.0&'
            f'query={request.quote(query)}&reg=1&regions={self.regions}&'
            'resultset=catalog&sort=popular&spp=32&sppFixGeo=4&'
            'suppressSpellcheck=false'
        )
        print(query)
        response = self.get_url(url)
        if response.status_code == 200:
            if response.text == '':
                return self.change_query()
            try:
                data = json.loads(r"{}".format(response.text))
                self.parse_search(data)
            except JSONDecodeError as e:
                self.notify('JSONDecodeError ' + query)
                print('JSONDecodeError', e, url)
                self.change_query()
            except Exception as e:
                print('except', str(e))
        else:
            self.notify('404 ' + query)
            return self.change_query()

    def crawl(self):
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog?'
            f'appType=1&couponsGeo={self.couponsGeo}&curr=rub&'
            f'dest={self.dest}&emp=0&lang=ru&locale=ru&'
            f'pricemarginCoeff=1.0&reg=1&regions={self.regions}&'
            f'sort=popular&spp=25&page={self.page}&{self.category.wb_query}'
        )
        print(self.category.name, self.page)

        response = self.get_url(url)

        if response.status_code == 200:
            if response.text == '':
                return self.change_category()
            try:
                data = json.loads(r"{}".format(response.text))
                self.parse_catalog(data)
            except JSONDecodeError as e:
                self.notify('JSONDecodeError ' + self.category.name + ' ' + str(self.page))
                print('JSONDecodeError', e, url)
            except Exception as e:
                print('except', str(e))
        else:
            self.notify('404 ' + self.category.name)
            return self.change_category()

    def change_query(self):
        self.query.parsed_at = datetime.utcnow()
        self.query.save()
        self.get_query()

    def change_category(self):
        self.category.last_parsed_page_at = datetime.utcnow()
        self.category.parsed_at = datetime.utcnow()
        self.category.save()
        self.get_category()

    def get_details(self, ids):
        ids = ';'.join([str(id) for id in ids])
        url = (
            f'https://card.wb.ru/cards/detail?spp=25&'
            f'regions={self.regions}&pricemarginCoeff=1.0&reg=1&appType=1&'
            f'emp=0&locale=ru&lang=ru&curr=rub&couponsGeo={self.couponsGeo}&'
            f'dest={self.dest}&nm={ids}'
        )
        response = self.get_url(url)
        if response.status_code == 200:
            if response.text == '':
                self.notify('get_details empty')
                return []
            try:
                # data = response.json()
                data = json.loads(r"{}".format(response.text))
                return data['data']['products']
            except JSONDecodeError as e:
                self.notify('JSONDecodeError ' + str(e))
                print('JSONDecodeError', e, response)
            except Exception as e:
                print('except', str(e))
                self.notify('Exception ' + str(e))
        return []

    def text_process(self, product):
        doc = nlp(product.name)
        root = [w for w in doc if w.dep_ == 'ROOT'][0]
        if root.tag_ != 'NOUN':
            nsubj = [w for w in doc if w.dep_ == 'nsubj']
            if len(nsubj):
                root = nsubj[0]
        product.root = root.lemma_
        features = list(set([w.lemma_ for w in doc if w.tag_ == 'ADJ' and len(w.lemma_) > 1]))
        features.sort()
        product.features = features
        if len(doc.ents):
            product.entity = doc.ents[0].lemma_

    def check_unique(self, product):
        print(product.articul)
        Product.objects.filter(articul=product.articul).exclude(
            id=product.id).delete()
        product.check_articul = True
        product.save()

    def parse_products(self, products):
        print('products:', len(products))
        ids = [p['id'] for p in products]
        details = self.get_details(ids)
        print('details: ', len(details))
        for index, item in enumerate(products):
            try:
                product = Product.objects.get(articul=item['id'])
                last_sale = product.sale_set.first()
            except Content.DoesNotExist:
                product = None
                last_sale = None
            price = item.get('salePriceU') / 100
            detail = [detail for detail in details if detail['id'] == item['id']]
            if len(detail):
                detail = detail[0]
                sizes = detail.get('sizes', [])
                quantity = sum([
                    sum(
                        [stock.get('qty', 0) for stock
                         in size.get('stocks', [])]
                    ) for size in sizes
                ])
                sales = 0
            else:
                detail = None
                quantity = None
                sales = 0

            if product and detail:
                # self.check_unique(product)
                if last_sale.date != datetime.now().date():
                    # Если последняя цена вчерашняя то посчитать разницу остатков и
                    # записать как количество продаж
                    sales = product.quantity - quantity
                    # если цифра отрицательная то вероятно поступление
                    # на склад и расчет не получится
                    if sales < 0:
                        sales = 0
                else:
                    sales = 0

                if product.name != item['name'].strip():
                    product.name = item['name'].strip()
                    self.text_process(product)

                product.name = item['name']
                product.brand = item['brand']
                product.brand_id = item['siteBrandId']
                product.subject_id = item['subjectId']
                product.rating = item['rating']
                product.feedbacks = item['feedbacks']
                product.is_new = item.get('isNew', False)

                product.price = price
                product.priceU = item.get('priceU') / 100
                product.quantity = quantity
                product.sales = sales
                product.parsed_at = datetime.utcnow()

                if self.query is None:
                    product.category_name = self.category.name
                    product.category_id = self.category.id
                    product.category_wb_id = self.category.wb_id

                if last_sale and last_sale.date.date() == datetime.now().date():
                    pass
                else:
                    product.sale_set.create(
                        sales=sales,
                        price=price,
                        profit=sales * price,
                        quantity=quantity,
                        date=datetime.utcnow()
                    )

                if self.query is None and self.category.wb_id not in product.categories:
                    product.categories.append(self.category.wb_id)

                last_sales = product.sale_set.all()[:30]
                now = datetime.utcnow()
                current_hom_start = (now - timedelta(days=15)).replace(
                    hour=0, minute=0, second=0, microsecond=0)
                last_hom_start = current_hom_start - timedelta(days=15)
                last_hom_sales = 0
                current_hom_sales = 0
                hom_sales_growth = 0
                last_hom_profit = 0
                current_hom_profit = 0
                hom_profit_growth = 0
                if len(last_sales):
                    # HOM
                    last_hom_data = [sales for sales in last_sales
                                     if sales.date >= last_hom_start
                                     and sales.date < current_hom_start]
                    last_hom_sales = sum([(s.sales or 0) for s
                                          in last_hom_data])
                    last_hom_profit = sum([(s.sales or 0) * (s.price or product.price or 0) for s
                                           in last_hom_data])
                    current_hom_data = [sales for sales in last_sales
                                        if sales.date >= current_hom_start]
                    current_hom_sales = sum([(s.sales or 0) for s
                                             in current_hom_data])
                    current_hom_profit = sum(
                        [(s.sales or 0) *
                         (s.price or product.price or 0) for
                         s in current_hom_data])
                    if last_hom_sales != 0:
                        hom_sales_growth = int(
                            current_hom_sales /
                            last_hom_sales * 100)
                    else:
                        hom_sales_growth = 0
                    if last_hom_profit != 0:
                        hom_profit_growth = int(
                            current_hom_profit /
                            last_hom_profit * 100)
                    else:
                        hom_profit_growth = 0

                product.decada_sales_growth = decada_sales_growth
                product.current_decada_sales = current_decada_sales
                product.last_decada_sales = last_decada_sales
                product.current_decada_profit = current_decada_profit
                product.last_decada_profit = last_decada_profit
                product.last_hom_sales = last_hom_sales
                product.current_hom_sales = current_hom_sales
                product.hom_sales_growth = hom_sales_growth
                product.last_hom_profit = last_hom_profit
                product.current_hom_profit = current_hom_profit
                product.hom_profit_growth = hom_profit_growth
                product.save()

            elif detail and item['name'].strip():
                product = Product(
                    articul=item['id'],
                    name=item['name'],
                    brand=item['brand'],
                    brand_id=item['siteBrandId'],
                    category_name=self.category.name,
                    category_id=self.category.id,
                    category_wb_id=self.category.wb_id,
                    categories=[self.category.wb_id],
                    subject_id=item['subjectId'],
                    rating=item['rating'],
                    feedbacks=item['feedbacks'],
                    is_new=item.get('isNew', False),
                    price=price,
                    sales=sales,
                    priceU=(item.get('priceU') / 100),
                    quantity=quantity,
                    parsed_at=datetime.utcnow(),
                )
                self.text_process(product)
                product.save()
                product.sale_set.create(
                    quantity=quantity,
                    sales=sales,
                    price=price,
                    profit=sales * price,
                    date=datetime.utcnow()
                )

    def parse_search(self, data):
        print('parse_search', self.query)
        if len(data.get('data', {}).get('products', [])) > 0:
            products = data['data']['products']
            ids = self.query.articuls + [p['id'] for p in products]
            self.query.articuls = ids
            self.query.save()
            self.parse_products(data['data']['products'])
            self.query.last_parsed_page = self.page
            self.query.save()
            self.page += 1
            if self.page > 5:
                self.change_query()
            else:
                self.get_query()
        else:
            self.change_query()

    def parse_catalog(self, data):
        print('parse_catalog', self.category.name, self.page)
        if len(data.get('data', {}).get('products', [])) > 0:
            self.parse_products(data['data']['products'])
            self.category.last_parsed_page = self.page
            self.category.last_parsed_page_at = datetime.utcnow()
            self.category.save()
            self.page += 1
            if self.page > 100:
                self.change_category()
            else:
                self.get_category()
        else:
            self.change_category()

    def get_avg(self, values):
        if len(values):
            return sum([sum(value) / len(value) for value in values if len(value)]) / len(values)
        else:
            return 0

    def get_sum(self, values):
        return sum([sum(value) for value in values])

    def set_period_dates(self):
        self.end_prev_period = (datetime.now() - timedelta(days=15)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.start_prev_period = self.end_prev_period - timedelta(days=15)

    def calculate_category(self, category):
        # Путь 1 (товары с высоким оборотом):
        # 1. В каждой категории нижнего уровня отбираются топ 50 товаров по
        # обороту с сортировкой от большего к меньшему
        # Условия отбора:
        # - Оборот первого товара не меньше 500к, оборот десятого товара не
        # меньше 100к
        # - Количество товаров в категории: не более 300
        # - Количество товаров с продажами: не меньше 20%
        # - Средний чек в категории месяц назад и сейчас отличается не более
        # чем на +-10%
        # - Оборот в категории месяц назад и сейчас отличается
        # не более чем на +-10%
        # Если все условия пройдены - то информация о нише и топ 50 товарах
        # отправляются в раздел ""топ категории"" для декады делим месяц на три
        self.set_period_dates()
        products = Product.objects.prefetch_related('sale_set').filter(
            categories__contains=[category.wb_id])
        # last_sales = product.sale_set.all()[:30]
        category.products_count = products.count()
        print(category.name, category.products_count)
        if category.products_count > 10:
            top_products = products.order_by('-current_hom_sales')[0:50]
            category.products_with_sales = products.filter(
                current_hom_sales__gt=0).count()
            category.profit_period = self.get_sum([
                [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
                 for s in p.sizes if s.date >= self.end_prev_period]
                for p in products])
            category.profit_prev_period = self.get_sum([
                [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
                 for s in p.sizes if s.date >= self.start_prev_period and
                 s.date < self.end_prev_period]
                for p in products])

            category.sellers = len(list(set([p.brand_id for p in products])))
            category.sellers_with_sales = len(list(set([
                p.brand_id for p
                in products.filter(current_hom_sales__gt=0)])))
            category.avg_price_prev_period = self.get_avg([
                [s.price for s in p.sizes
                 if s.price and s.date >= self.start_prev_period and
                 s.date < self.end_prev_period] for p in products])
            category.avg_price_period = self.get_avg([
                [s.price for s in p.sizes
                 if s.price and s.date >= self.end_prev_period]
                for p in products])
            category.sales_period = self.get_sum([
                [(s.sales or 0) for s in p.sizes
                 if s.date >= self.end_prev_period] for p in products])

            category.first_product_price = top_products[0].price
            category.first_product_sales = top_products[0].current_hom_sales
            category.first_product_profit = (
                (top_products[0].current_hom_sales or 0)
                *
                (top_products[0].price or 0)
            )
            category.ten_product_price = top_products[9].price
            category.ten_product_sales = top_products[9].current_hom_sales
            category.ten_product_profit = (
                (top_products[9].current_hom_sales or 0)
                *
                (top_products[9].price or 0)
            )
            category.rel_sellers = category.sellers_with_sales / category.sellers
            category.rel_sales = category.products_with_sales / category.products_count

            if category.first_product_hom_profit >= self.profit_first_top:
                category.first_product_profit_top = True
            if category.ten_product_hom_profit >= self.profit_ten_top:
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
                    category.products_count <= 2500 and
                    category.first_product_profit_top and
                    category.ten_product_profit_top and
                    category.rel_sales_top and
                    category.avg_price_top and
                    category.profit_top):
                category.top = True
        category.calculated = True
        category.save()
        print(category)

    def calculate_queries(self):
        query = Query.objects.filter(
            current_parsing_id=self.config.current_parsing_id,
            products_count__gte=1,
        ).exclude(calculated=True).first()
        while query:
            self.calculate_query(query)
            query = Query.objects.filter(
                current_parsing_id=self.config.current_parsing_id,
                products_count__gte=1,
            ).exclude(calculated=True).first()
        self.config.queries_calculated = True
        self.config.save()
        self.processing()

    def calculate_categories(self):
        category = Category.objects.filter(parse=True).exclude(
            calculated=True).first()
        while category:
            self.calculate_category(category)
            category = Category.objects.filter(parse=True).exclude(
                calculated=True).first()
        self.config.categories_calculated = True
        self.config.save()
        self.processing()

    def calculate_query(self, query):
        products = Product.objects.prefetch_related('sale_set').filter(
            articul__in=query.articuls
        )
        # .fields(slice__sizes=[-30, 30]).order_by('-current_hom_sales')
        products_count = products.count()
        if products_count >= 10:
            query.first_product_hom_profit = (
                (products[0].current_hom_sales or 0)
                *
                (products[0].price or 0)
            )
            query.ten_product__profit = (
                (products[9].current_hom_sales or 0)
                *
                (products[9].price or 0)
            )
            query.products_with_sales = products.filter(
                current_hom_sales__gt=0).count()
            query.rel_products_with_sales = int(query.products_with_sales * 100 / query.products_count)
            query.avg_price_prev_period = self.get_avg(
                [[s.price for s in p.sizes if s.price
                  and s.date >= self.start_prev_period
                  and s.date < self.end_prev_period] for p in products]
            )
            query.avg_price_period = self.get_avg(
                [[s.price for s in p.sizes if s.price
                  and s.date >= self.end_prev_period] for p in products]
            )
            query.profit_prev_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes
                  if s.date >= self.start_prev_period
                  and s.date < self.end_prev_period
                  ]
                 for p in products]
            )
            query.profit_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes if s.date >= self.end_prev_period]
                 for p in products]
            )
            # Оборот первого не меньше 500к -> 300к
            if query.first_product_hom_profit >= 300000 / 2:
                query.first_product_profit_top = True
            # оборот десятого не меньше 100к -> 70к
            if query.ten_product_hom_profit >= 70000 / 2:
                query.ten_product_profit_top = True
            # Количество товаров с продажами: не меньше 20%
            if query.products_with_sales / products.count() >= 1/5:
                query.products_with_sales_top = True
            # Средний чек в категории месяц назад и сейчас
            # отличается не более чем на +/- 10% -> 40%
            if (
                    query.avg_price_period >=
                    query.avg_price_prev_period * 0.6 and
                    query.avg_price_period <=
                    query.avg_price_prev_period * 1.4):
                query.avg_price_top = True
            # Оборот в категории месяц назад и сейчас отличается
            # не более чем на +/- 10%
            if (
                    query.profit_period >= query.profit_prev_period * 0.6 and
                    query.profit_period <= query.profit_prev_period * 1.4):
                query.profit_top = True
            if (
                    query.products_count <= 2500 and
                    query.first_product_profit_top and
                    query.ten_product_profit_top and
                    query.products_with_sales_top and
                    query.avg_price_top and
                    query.profit_top):
                query.top = True
        query.calculated = True
        query.save()
        print(query)

    def calculate_products(self):
        # "Товары в этот раздел отбираются по следующему принципу:
        # 1. В каждой категории нижнего уровня отбираются топ 50 товаров
        # по росту оборота в процентах.
        # Условие отбора:
        # - Оборот товара в первом периоде должен быть больше 10 000
        # 2. Алгоритм вычленяет главное слово и характеристику для
        # каждого товара из топ 50 и объединяет товары по главному слову
        # и характеристике и составляет их в одну таблицу
        # 3. Алгоритм забивает каждое наименование в поиск на маркетплейсе
        # Условие отбора:
        # - товаров по запросу должно быть не больше 1000
        # 3. Составляется таблица товаров из выдачи с сортировкой по обороту
        # от большего к меньшему
        # Условия отбора:
        # - Количество товаров с продажами: не меньше 40%
        # - Оборот первого не меньше 500к, оборот десятого не меньше 100к
        # Если все условия соблюдены, первые 2 товара из объединенного списка
        # (или один товар, если он не объединенный) попадают в таблицу ""Топ товаров""
        # Операция повторяется с каждым товаром из таблицы с объединенными
        # товарами, составленной в пункте 2
        #
        # В этой странице открывается таблица со следующеми данными:
        # 1. Название товара
        # 2. Фото
        # 3. Ссылка
        # 4. Рейтинг
        # 5. Продавец
        # 6. Бренд
        # 7. Оборот в текущем периоде, в скобках: увеличение оборота в процентах относительно прошлого периода
        # 8. Цена (после скидки)
        # 9. Продажи (в штуках)
        # 10. Количество товаров на складе
        # 11. Упущенный оборот из-за обнуления остатков(?)
        # 12. Перспективность ниши (?)
        # 13. Ключевые слова (?)
        # "Здесь и дальше период оценки 30 дней:
        # - Если сравниваются периоды продаж: то первые 15 дней и
        # следующие 15 дней , без привязки к календарным месяцам
        # - Если сравнивается средняя цена в категории, то сравнивается
        # средняя цена 30 дней назад и на данный момент"
        # "
        category = Category.objects.filter(parse=True).exclude(
            products_calculated=True).first()
        while category:
            self.calculate_category_products(category)
            category = Category.objects.filter(parse=True).exclude(
                products_calculated=True).first()
        self.config.products_calculated = True
        self.config.save()
        self.processing()

    def calculate_category_products(self, category):
        # тут все расчёты
        category.products_calculated = True
        category.save()


# parser = Parser()
