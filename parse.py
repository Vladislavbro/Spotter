import requests
from models import Categories, Products, Config, Queries
from time import sleep
from datetime import datetime, timedelta
import time
import sys
import re
import json
from telegram import Bot
import sys, traceback
from json import JSONDecodeError
from proxies import proxies
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

    def __init__(self):
        super(Parser, self).__init__()
        self.config = Config.objects.first()
        # self.product_unique()
        self.start_parsing()
        # self.get_categories()
        # self.create_queries()

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

    def start_parsing(self):
        if self.config.parsing_done is not True:
            self.get_category()
        elif self.config.queries_done is not True:
            self.get_query()
        elif self.config.current_parsing_date.date() != datetime.utcnow().date():
            self.config.parsing_done = False
            self.config.queries_done = False
            date = datetime.utcnow()
            self.config.current_parsing_date = date
            self.config.current_parsing_id = int(date.timestamp())
            self.config.save()
            self.get_category()

    def create_queries(self):
        # Queries.objects().delete()
        categories = Categories.objects(parse=True)
        for category in categories:
            self.category = category
            products = Products.objects(categories__in=[self.category.wb_id])
            # top_products = products.filter(last_decada_profit__gte=profit_last_decada).order_by('-current_decada_sales')[0:50]
            top_products = products.filter(
                current_decada_sales__gt=0).order_by('-current_decada_sales')[0:50]
            for top in top_products:
                features = top.features
                features.sort()
                q = Queries.objects(
                    root=top.root,
                    features=features,
                    current_parsing_id=self.config.current_parsing_id
                ).first()
                if q is None:
                    q = Queries(
                        root=top.root,
                        features=features,
                        category_id=category.id,
                        current_parsing_id=self.config.current_parsing_id
                    )
                    q.save()
                    print(q.root, q.features)

    def update_category(self, child):
        category = Categories.objects(wb_id=child['id']).first()
        if category is None:
            category = Categories(wb_id=child['id'])
        category.name = child.get('name')
        category.shard = child.get('shard')
        category.query = child.get('query')
        category.parent = child.get('parent')
        category.query = child.get('query')
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
        Categories.objects.update(
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
        self.query = Queries.objects.filter(
            current_parsing_id=self.config.current_parsing_id,
            parsed_at=None,
            root__ne=None
        ).first()
        if self.query is None:
            self.notify('Парсинг запросов закончился')
            self.config.queries_done = True
            self.config.save()
            return self.caclulate()
        else:
            self.category = self.query.category_id
            if self.query.last_parsed_page and self.query.last_parsed_page < 5:
                self.page = self.query.last_parsed_page + 1
            else:
                self.page = 1
            return self.query_crawl()

    def get_category(self):
        self.category = Categories.objects.filter(parsed_at=None,
                                                  parse=True).first()
        if self.category is None:
            self.notify('Парсинг категорий закончился')
            Categories.objects(parse=True).update(
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
        # url2 = (
        #     'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&'
        #     f'couponsGeo={self.couponsGeo}&curr=rub&dest={self.dest}&'
        #     f'emp=0&lang=ru&locale=ru&page={self.page}&pricemarginCoeff=1.0&'
        #     f'query={query}&reg=1&regions={self.regions}&resultset=filters&'
        #     'sort=popular&spp=32&sppFixGeo=4&suppressSpellcheck=false'
        # )
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
            f'sort=popular&spp=25&page={self.page}&{self.category.query}'
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
        Products.objects(articul=product.articul, id__ne=product.id).delete()
        product.check_articul = True
        product.save()

    def parse_products(self, products):
        print('products:', len(products))
        ids = [p['id'] for p in products]
        details = self.get_details(ids)
        print('details: ', len(details))
        for index, item in enumerate(products):
            product = Products.objects(
                articul=item['id']
            ).fields(slice__sizes=[-2, 2]).first()
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
                if product.sizes[-1].date != datetime.now().date():
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
                    product.save()
                Products.objects(id=product.id).update_one(
                    set__name=item['name'],
                    set__brand=item['brand'],
                    set__brand_id=item['siteBrandId'],
                    set__subject_id=item['subjectId'],
                    set__rating=item['rating'],
                    set__feedbacks=item['feedbacks'],
                    set__is_new=item.get('isNew', False),
                    set__data=item,
                    set__price=price,
                    set__priceU=item.get('priceU') / 100,
                    set__quantity=quantity,
                    set__sales=sales,
                    set__parsed_at=datetime.utcnow(),
                )
                if self.query is None:
                    Products.objects(id=product.id).update_one(
                        set__category_name=self.category.name,
                        set__category_id=self.category.id,
                        set__category_wb_id=self.category.wb_id,
                    )
                if len(product.sizes) and product.sizes[-1].date.date() == datetime.now().date():
                    pass
                else:
                    Products.objects(id=product.id).update_one(
                        push__sizes={
                            'sales': sales,
                            'price': price,
                            'profit': sales * price,
                            'quantity': quantity,
                            'date': datetime.utcnow()
                        }
                    )
                # if self.query:
                #     if str(self.query.id) not in product.queries:
                #         Products.objects(id=product.id).update_one(
                #             push__queries=str(self.query.id)
                #         )
                if self.query is None and self.category.wb_id not in product.categories:
                    Products.objects(id=product.id).update_one(
                        push__categories=self.category.wb_id
                    )
                product = Products.objects(
                    articul=item['id']
                ).fields(slice__sizes=[-20, 20]).first()
                now = datetime.utcnow()
                current_decada_start = (now - timedelta(days=10)).replace(
                    hour=0, minute=0, second=0, microsecond=0)
                last_decada_start = current_decada_start - timedelta(days=10)
                if len(product.sizes):
                    last_decada_data = [sales for sales in product.sizes
                                        if sales.date >= last_decada_start
                                        and sales.date < current_decada_start]
                    last_decada_sales = sum([(s.sales or 0) for s
                                             in last_decada_data])
                    last_decada_profit = sum([(s.sales or 0) * (s.price or product.price or 0) for s
                                             in last_decada_data])
                    current_decada_data = [sales for sales in product.sizes
                                           if sales.date >= current_decada_start]
                    current_decada_sales = sum([(s.sales or 0) for s
                                                in current_decada_data])
                    current_decada_profit = sum(
                        [(s.sales or 0) *
                         (s.price or product.price or 0) for
                         s in current_decada_data])

                    if last_decada_sales != 0:
                        decada_sales_growth = int(
                            current_decada_sales /
                            last_decada_sales * 100)
                    else:
                        decada_sales_growth = 0
                else:
                    last_decada_sales = 0
                    current_decada_sales = 0
                    decada_sales_growth = 0
                    last_decada_profit = 0
                    current_decada_profit = 0
                Products.objects(id=product.id).update_one(
                    set__decada_sales_growth=decada_sales_growth,
                    set__current_decada_sales=current_decada_sales,
                    set__last_decada_sales=last_decada_sales,
                    set__current_decada_profit=current_decada_profit,
                    set__last_decada_profit=last_decada_profit,
                )
            elif detail and item['name'].strip():
                product = Products(
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
                    data=item,
                    price=price,
                    sales=sales,
                    priceU=(item.get('priceU') / 100),
                    quantity=quantity,
                    parsed_at=datetime.utcnow(),
                )
                product.sizes.create(
                    quantity=quantity,
                    sales=sales,
                    price=price,
                    profit=sales * price,
                    date=datetime.utcnow())
                self.text_process(product)
                product.save()

    def parse_search(self, data):
        print('parse_search', self.query)
        if len(data.get('data', {}).get('products', [])) > 0:
            products = data['data']['products']
            ids = self.query.articuls + [p['id'] for p in products]
            Queries.objects(id=self.query.id).update_one(set__articuls=ids)
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

    def caclulate(self):
        self.notify('Расчёт начался')
        queries = Queries.objects(
            current_parsing_id=self.config.current_parsing_id)
        for query in queries:
            self.calculate_query(query)

    def calculate_query(self, query):
        products = Products.objects(articul__in=query.articuls)
        if products.count() >= 10:
            first_product_decada_profit = (
                (products[0].current_decada_sales or 0)
                *
                (products[0].price or 0)
            )
            ten_product_decada_profit = (
                (products[9].current_decada_sales or 0)
                *
                (products[9].price or 0)
            )
            products_with_sales = products.filter(
                current_decada_sales__gt=0).count()
            avg_price_prev_period = self.get_avg(
                [[s.price for s in p.sizes if s.price
                  and s.date >= self.start_prev_period
                  and s.date < self.end_prev_period] for p in products]
            )
            avg_price_period = self.get_avg(
                [[s.price for s in p.sizes if s.price
                  and s.date >= self.end_prev_period] for p in products]
            )
            profit_prev_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes
                  if s.date >= self.start_prev_period
                  and s.date < self.end_prev_period
                  ]
                 for p in products]
            )
            profit_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sizes if s.date >= self.end_prev_period]
                 for p in products]
            )
            sellers = len(list(set([p.brand_id for p in products])))
            sellers_with_sales = len(list(set(
                [p.brand_id for p
                 in products.filter(current_decada_sales__gt=0)]
            )))
            sales_period = self.get_sum(
                [[(s.sales or 0) for s in p.sizes
                  if s.date >= self.end_prev_period] for p in products])
            calc = dict()
            # Оборот первого не меньше 500к
            if first_product_decada_profit < self.profit_first_top:
                calc['profit_first_top'] = False
            # оборот десятого не меньше 100к
            if ten_product_decada_profit < self.profit_ten_top:
                calc['profit_ten_top'] = False
            # Количество товаров с продажами: не меньше 20%
            if products_with_sales / products.count() < 1/5:
                calc['products_with_sales'] = False
            # Средний чек в категории месяц назад и сейчас
            # отличается не более чем на +/- 10%
            if avg_price_period < avg_price_prev_period * 0.9:
                calc['avg_price_diff'] = False
            if avg_price_period > avg_price_prev_period * 1.1:
                calc['avg_price_diff'] = False
            # Оборот в категории месяц назад и сейчас отличается
            # не более чем на +/- 10%
            if profit_period < profit_prev_period * 0.9:
                calc['profit_period'] = False
            if profit_period > profit_prev_period * 1.1:
                calc['profit_period'] = False
            query.params = calc
            query.save()


parser = Parser()
