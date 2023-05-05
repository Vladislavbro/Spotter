import requests
# from api.mongo_models import Categories, Products, Config, Queries
from api.models import Category, Product, Config, Query
from time import sleep
from datetime import datetime, timedelta, timezone
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
import asyncio
import pytz

utc = pytz.UTC
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
nlp = spacy.load('ru_core_news_md')

user_agent_rotator = UserAgent()
TOKEN = '6161677884:AAE8uT0XWRVXr7SbGIjVTP3Ik6BhsDm8Z5I'
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
    adminIds = [259180458, 190056210]
    config = None
    end_prev_period = None
    start_prev_period = None
    profit_first_top = 500000 / 2
    profit_ten_top = 100000 / 2
    wirehouses = [169537, 205985, 214951, 214110, 146666, 207399, 6149,
                  118365, 1680, 213651, 117419, 216462, 152611, 210557, 6140,
                  204223, 117414, 217390, 203632, 115651, 209209, 206844,
                  216745, 118019, 117442, 205104, 159402, 130744, 205349,
                  274562, 6144, 117456, 158311, 6156, 144649, 204939, 161003,
                  133858, 203799, 117819, 206236, 1193, 140302, 106476,
                  205228, 207404, 204615, 158751, 117986, 206708, 207803,
                  217081, 169872, 210127, 158140, 207022, 131643, 120762,
                  507, 206348, 205205, 210515, 1733, 160030, 204952, 208277,
                  208941, 172430, 168458, 149445, 203631, 207016, 207743,
                  211622, 211415, 206385, 206298, 211644, 209211]

    def __init__(self):
        super(Parser, self).__init__()
        self.config = Config.objects.first()
        self.set_period_dates()
        self.processing()

    def get_wirehouses(self):
        url = "https://seller.wildberries.ru/ns/distribution-offices/distribution-offices/api/v1/office/getAllMarketplace"
        payload = json.dumps({
          "params": {
            "filters": [
              "isSupply"
            ]
          },
          "jsonrpc": "2.0",
          "id": "json-rpc_8"
        })
        headers = {
          'Cookie': 'BasketUID=da722e75-870f-400d-b096-bdb9d7960e94; _wbauid=199913131664012470; _ga=GA1.2.1918642823.1664012471; ___wbu=265a9450-8a5b-4e24-b416-7c18f4ba3f04.1664012470; locale=ru; x-supplier-id=d4607f1f-5b74-48e2-898e-db7ee2d7f7f0; x-supplier-id-external=d4607f1f-5b74-48e2-898e-db7ee2d7f7f0; WILDAUTHNEW_V3=732517BF2ED31BEBF20A5BD431CA9404CBE84BE113CB3733067195530FAC8EA57349678D4D71250BAA1EE7CAFDFBBF1BAC8C94A43F99B8AF48B44CEB5CBA7FCA7933FBD5C152D3D7246C1E4CAE8DD92163F809D9BD9037F461ABB5202A9DCDBCF4DCC1B5C0875D2B479C1E2FE4347C6A7D75888B91C6F778812C36FA911C158E2686B2F91369A473381459EC34A5116B5CF8E1F1D217C9093A292BAF0AAF39C778294F3021D4618BD066BDE66CBFD2A0C7774EE8553E1DFFA3736196F10F72532464346070BE81EA50B998CF91A439F75D444E67DFF90A9CA8DE765D7360729E3B20A9A85812A8F197BB2D6F5F6DC8B94B898986D29BC5D0B2FB6EB23020E966D1E6BE8FFB5AF2F373850B5073BC6631BD103ED5AE27A1BAD19E66BA82BBD2509FB7ACA207F4B6F1497200ECDBFC2384EA322297; WBToken=Apjb3xqygIDEDLLOieIMQv0FyZ2z9KJgryyA7xndg1yw-7o1dr5mJ7U6T_CEfEMxVRFzVBUigmeUWoxtYhUhr90KqQvk3FvvKdw2Vtvli-pewA',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            self.wirehouses = [w['origid'] for w
                               in data['result']['resp']['data']]

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
            # elif self.config.queries_done is not True:
            #     self.notify('Парсинг запросов начался')
            #     self.get_query()
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
            date = datetime.now(timezone.utc)
            self.config = Config(
                current_parsing_id=int(date.timestamp()),
            )
            self.config.save()
            self.notify('Новый цикл начался')
            self.get_category()

    def create_queries(self):
        self.notify('Создаются поисковые запросы')
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
                loop = asyncio.new_event_loop()
                loop.run_until_complete(
                    bot.send_message(chat_id=id, text=text)
                )
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
            self.category = Category.objects.get(pk=self.query.category_id)
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
            return self.calculate_query()
        else:
            if self.category.last_parsed_page:
                self.page = self.category.last_parsed_page + 1
            else:
                self.category.start_parsing_at = datetime.now(timezone.utc)
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
                # self.notify('get_query_detail JSONDecodeError ' + query)
                print('get_query_detail JSONDecodeError', e, url)
            except Exception as e:
                print('except', str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('exc_type, fname, exc_tb.tb_lineno', exc_type, fname, exc_tb.tb_lineno)
        else:
            print(f'get_query_detail {response.status_code} {query}')
            # self.notify()

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
                # self.notify('JSONDecodeError ' + query)
                print('JSONDecodeError', e, url)
                self.change_query()
            except Exception as e:
                print('except', str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('exc_type, fname, exc_tb.tb_lineno', exc_type, fname, exc_tb.tb_lineno)
        else:
            # self.notify('404 ' + query)
            return self.change_query()

    def crawl(self):
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog?'
            f'appType=1&couponsGeo={self.couponsGeo}&curr=rub&'
            f'dest={self.dest}&emp=0&lang=ru&locale=ru&'
            f'pricemarginCoeff=1.0&reg=1&regions={self.regions}&'
            f'sort=popular&spp=25&page={self.page}&{self.category.wb_query}'
        )
        response = self.get_url(url)
        if response.status_code == 200:
            if response.text == '':
                print('change_category')
                return self.change_category()
            try:
                data = json.loads(r"{}".format(response.text))
                self.parse_catalog(data)
            except JSONDecodeError as e:
                # self.notify('JSONDecodeError ' + self.category.name + ' ' + str(self.page))
                print('JSONDecodeError', e, url)
            except Exception as e:
                print('except', str(e))
        else:
            # self.notify('404 ' + self.category.name)
            return self.change_category()

    def change_query(self):
        self.query.parsed_at = datetime.now(timezone.utc)
        self.query.save()
        self.get_query()

    def change_category(self):
        self.category.last_parsed_page_at = datetime.now(timezone.utc)
        self.category.parsed_at = datetime.now(timezone.utc)
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
                # self.notify('get_details empty')
                return []
            try:
                # data = response.json()
                data = json.loads(r"{}".format(response.text))
                return data['data']['products']
            except JSONDecodeError as e:
                # self.notify('JSONDecodeError ' + str(e))
                print('JSONDecodeError', e, response)
            except Exception as e:
                print('except', str(e))
                # self.notify('Exception ' + str(e))
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

    def get_old_data(self, product):
        if product.mongo_transfered is not True:
            url = f'https://m.spotter.fun/api/products/{product.articul}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('product'):
                    for size in data['product'].get('sizes', []):
                        if size.get('profit') is not None:
                            date = datetime.fromtimestamp(
                                size['date']['$date'] / 1000)
                            date = date.replace(tzinfo=timezone.utc)
                            product.sale_set.create(
                                date=date,
                                quantity=size.get('quantity', 0),
                                sales=size.get('sales', 0),
                                profit=size.get('profit', 0),
                                price=size.get('price', 0),
                            )
            product.mongo_transfered = True

    def product_calculate(self, product):
        last_sales = product.sale_set.all()[:30].values()

        now = datetime.now(timezone.utc)
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
            last_hom_data = [sale for sale in last_sales
                             if sale['date'] >= last_hom_start and
                             sale['date'] < current_hom_start]
            last_hom_sales = sum([s.get('sales', 0) for s in last_hom_data])
            last_hom_profit = sum([s.get('sales', 0) * (s.get('price', 0)
                                                        or product.price) for s
                                   in last_hom_data])
            current_hom_data = [sale for sale in last_sales
                                if sale['date'] >= current_hom_start]
            current_hom_sales = sum([s.get('sales', 0) for s
                                     in current_hom_data])
            current_hom_profit = sum(
                [s.get('sales', 0) * (s.get('price', 0) or product.price) for
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
        product.last_hom_sales = last_hom_sales
        product.current_hom_sales = current_hom_sales
        product.hom_sales_growth = hom_sales_growth
        product.last_hom_profit = last_hom_profit
        product.current_hom_profit = current_hom_profit
        product.hom_profit_growth = hom_profit_growth

    def parse_products(self, products):
        print('products:', len(products))
        ids = [p['id'] for p in products]
        details = self.get_details(ids)
        print('details: ', len(details))
        for index, item in enumerate(products):
            print('item[id]', item['id'])
            product = Product.objects.filter(articul=item['id']).first()
            if product:
                last_sale = product.sale_set.first()
            else:
                product = None
                last_sale = None
            price = item.get('salePriceU') / 100
            detail = [detail for detail in details if detail['id'] == item['id']]
            if len(detail):
                detail = detail[0]
                sizes = detail.get('sizes', [])
                quantity = 0
                quantity_fbo = 0
                quantity_fbs = 0
                for size in sizes:
                    for stock in size.get('stocks', []):
                        qty = stock.get('qty', 0)
                        quantity += qty
                        if stock.get('wh') in self.wirehouses:
                            quantity_fbo += qty
                        else:
                            quantity_fbs += qty
            else:
                detail = None
                quantity = None
                quantity_fbo = None
                quantity_fbs = None
            sales = 0
            sales_fbo = 0
            sales_fbs = 0

            if product and detail:
                # self.check_unique(product)
                if last_sale and last_sale.date.date() != datetime.now(timezone.utc).date():
                    # Если последняя цена вчерашняя то посчитать разницу остатков и
                    # записать как количество продаж
                    sales = product.quantity - quantity
                    if product.quantity_fbo is not None:
                        sales_fbo = product.quantity_fbo - quantity_fbo
                    if product.quantity_fbs is not None:
                        sales_fbs = product.quantity_fbs - quantity_fbs
                    # если цифра отрицательная то вероятно поступление
                    # на склад и расчет не получится
                    if sales < 0:
                        sales = 0
                    if sales_fbo < 0:
                        sales_fbo = 0
                    if sales_fbs < 0:
                        sales_fbs = 0

                # print('item[name]', item.get('name'))
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
                product.quantity_fbo = quantity_fbo
                product.quantity_fbs = quantity_fbs
                product.sales = sales
                product.sales_fbo = sales_fbo
                product.sales_fbs = sales_fbs
                product.parsed_at = datetime.now(timezone.utc)

                if self.query is None:
                    # print('self.category', self.category, self.category.name)
                    product.category_name = self.category.name
                    product.category_id = self.category.id
                    product.category_wb_id = self.category.wb_id

                if last_sale and last_sale.date.date() == datetime.now(timezone.utc).date():
                    pass
                else:
                    product.sale_set.create(
                        sales=sales,
                        sales_fbo=sales_fbo,
                        sales_fbs=sales_fbs,
                        price=price,
                        profit=sales * price,
                        profit_fbo=sales_fbo * price,
                        profit_fbs=sales_fbs * price,
                        quantity=quantity,
                        quantity_fbo=quantity_fbo,
                        quantity_fbs=quantity_fbs,
                        date=datetime.now(timezone.utc)
                    )

                if self.query is None and self.category.wb_id not in product.categories:
                    product.categories.append(self.category.wb_id)

                self.get_old_data(product)
                self.product_calculate(product)
                product.save()

            elif detail and item.get('name', '').strip():
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
                    # sales=sales,
                    # sales_fbo=sales_fbo,
                    # sales_fbs=sales_fbs,
                    priceU=(item.get('priceU') / 100),
                    quantity=quantity,
                    quantity_fbo=quantity_fbo,
                    quantity_fbs=quantity_fbs,
                    parsed_at=datetime.now(timezone.utc),
                )
                self.text_process(product)
                product.save()
                product.sale_set.create(
                    quantity=quantity,
                    quantity_fbo=quantity_fbo,
                    quantity_fbs=quantity_fbs,
                    # sales=sales,
                    # sales_fbo=sales_fbo,
                    # sales_fbs=sales_fbs,
                    price=price,
                    profit=sales * price,
                    profit_fbo=sales_fbo * price,
                    profit_fbs=sales_fbs * price,
                    date=datetime.now(timezone.utc)
                )
                print('get_old_data', product.articul)
                self.get_old_data(product)
                self.product_calculate(product)
                product.save()

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
            self.category.last_parsed_page_at = datetime.now(timezone.utc)
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
        self.end_prev_period = (datetime.now(timezone.utc) - timedelta(days=15)).replace(
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
        if category.products_count > 10 and category.products_count <= 2500:
            top_products = products.order_by('-current_hom_sales')[0:50]
            category.products_with_sales = products.filter(
                current_hom_sales__gt=0).count()
            category.profit_period = self.get_sum([
                [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
                 for s in p.sale_set.filter(date__gte=self.end_prev_period)]
                for p in products])
            category.profit_prev_period = self.get_sum([
                [s.profit or ((s.sales or 0) * (s.price or p.price or 0))
                 for s in p.sale_set.filter(
                     date__gte=self.start_prev_period,
                     date__lt=self.end_prev_period)]
                for p in products])

            category.sellers = len(list(set([p.brand_id for p in products])))
            category.sellers_with_sales = len(list(set([
                p.brand_id for p
                in products.filter(current_hom_sales__gt=0)])))
            category.avg_price_prev_period = self.get_avg([
                [s.price for s in p.sale_set.filter(
                    price__gt=0, date__gte=self.start_prev_period,
                    date__lt=self.end_prev_period)] for p in products])
            category.avg_price_period = self.get_avg([
                [s.price for s in p.sale_set.filter(
                    price__gt=0, date__gte=self.end_prev_period)]
                for p in products])
            category.sales_period = self.get_sum([
                [(s.sales or 0) for s in p.sale_set.filter(
                    date__gte=self.end_prev_period)
                 ] for p in products])

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

            if category.first_product_profit >= self.profit_first_top:
                category.first_product_profit_top = True
            if category.ten_product_profit >= self.profit_ten_top:
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
            root=query.root,
            features=query.features,
        ).order_by('-current_hom_sales')
        # products = Product.objects.prefetch_related('sale_set').filter(
        #     articul__in=query.articuls
        # ).order_by('-current_hom_sales')
        # .fields(slice__sizes=[-30, 30])
        products_count = products.count()
        print('calculate_query', products_count)
        query.products_count = products_count
        if products_count >= 10 and products_count <= 2500:
            query.first_product_hom_profit = (
                (products[0].current_hom_sales or 0)
                *
                (products[0].price or 0)
            )
            query.ten_product_hom_profit = (
                (products[9].current_hom_sales or 0)
                *
                (products[9].price or 0)
            )
            query.products_with_sales = products.filter(
                current_hom_sales__gt=0).count()
            query.rel_products_with_sales = int(query.products_with_sales * 100 / query.products_count)
            query.avg_price_prev_period = self.get_avg(
                [[s.price for s in p.sale_set.filter(
                    price__gt=0, date__gte=self.start_prev_period,
                    date__lt=self.end_prev_period)] for p in products]
            )
            query.avg_price_period = self.get_avg(
                [[s.price for s in p.sale_set.filter(
                    price__gt=0, date__gte=self.end_prev_period)] for p in products]
            )
            query.profit_prev_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sale_set.filter(
                      date__gte=self.start_prev_period,
                      date__lt=self.end_prev_period)]
                 for p in products]
            )
            query.profit_period = self.get_sum(
                [[s.profit or ((s.sales or 0) *
                               (s.price or p.price or 0))
                  for s in p.sale_set.filter(
                      date__gte=self.end_prev_period)]
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
