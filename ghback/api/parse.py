import requests
# from api.mongo_models import Categories, Products, Config, Queries
from django.forms.models import model_to_dict
from django.db.models import Sum, Avg, Q, Count
from api.models import (Category, Product, Config, Query, ProductStat, 
                        CategoryStat, CategorySaler)
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
import pymorphy2
from api.utils import get_scoring_productstats
import threading


morph = pymorphy2.MorphAnalyzer()
utc = pytz.UTC
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
nlp = spacy.load('ru_core_news_lg')

user_agent_rotator = UserAgent()
TOKEN = '6161677884:AAE8uT0XWRVXr7SbGIjVTP3Ik6BhsDm8Z5I'
bot = Bot(token=TOKEN)

sys.setrecursionlimit(10**6)

TIMEOUT = 0.5


class Parser(object):
    """docstring for Parser."""
    # regions = '68,64,83,4,38,80,33,70,82,86,75,30,69,1,48,22,66,31,40,71'
    regions = '80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,22,110,48,71,114'
    dest = '-1029256,-102269,-2162196,-1257786'
    couponsGeo = '12,3,18,15,21'
    page = 1
    category = None
    query = None
    adminIds = [259180458, 190056210]
    config = None
    end_prev_period = None
    start_prev_period = None
    profit_first_top = 500000
    profit_ten_top = 100000
    driver = None
    wirehouses = [169537, 205985, 117414, 209209, 117419, 210557, 
                  146666, 214951, 117866, 206844, 209207, 117442, 
                  205104, 205349, 159402, 130744, 204939, 144649, 
                  132508, 6156, 207390, 6144, 206236, 117456, 203799, 
                  118535, 6145, 216476, 1193, 117819, 161003, 140302, 
                  158311, 205228, 133858, 218210, 204615, 207803, 
                  206708, 117986, 158751, 169872, 210127, 206319, 158140, 
                  207404, 207022, 131643, 120762, 210515, 1733, 160030, 206348, 
                  205205, 507, 204203, 217081, 204952, 208277, 133533, 211470, 
                  168458, 158929, 149445, 172430, 203631, 208941, 211415, 
                  207743, 211622, 216566, 144154, 207016, 206968, 206298, 
                  206385, 213849, 211644, 209211, 215020, 218402]

    def __init__(self):
        super(Parser, self).__init__()
        self.config = Config.objects.first()
        # self.set_period_dates()
        # self.get_categories()
        self.processing()

    def get_category(self):
        self.category = Category.objects.filter(
            parsed_at=None, parse=True).first()
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
            Category.objects.exclude(parse=True).update(calculated=False)
            self.config.parsing_done = True
            self.config.save()
            return self.processing()
        else:
            if (self.category.categorysaler_set.count() == 0 and 
                    self.category.start_parsing_at is None):
                self.category.start_parsing_at = datetime.now(timezone.utc)
                self.category.save()
                self.get_salers()
            return self.get_category_salers()

    def get_salers(self):
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/v4/filters'
            f'?appType=1&curr=rub&dest=-1257786&filters=fsupplier&'
            f'spp=30&{self.category.wb_query}'
        )
        response = self.get_url(url)
        print('response', response.status_code)
        data = response.json()
        print('get_salers', self.category.name, len(data['data']['filters'][0]['items']))
        for saler in data['data']['filters'][0]['items']:
            # {'id': 228459, 'name': ' ИП ГРАБЧУК АНЖЕЛИКА НИКОЛАЕВНА', 'count': 7}
            CategorySaler.objects.create(
                category=self.category,
                wb_id=saler['id'],
                name=saler['name'],
                count=saler['count'],
            )

    def get_category_salers(self):
        # Получаем продавцов, отсортированных по 'count' в порядке убывания
        salers = list(CategorySaler.objects.order_by('-count'))

        # Если нет продавцов, обновляем 'parsed_at' для категории и переходим к следующей категории
        if not salers:
            self.category.parsed_at = datetime.now(timezone.utc)
            self.category.save()
            return self.get_category()

        # Обрабатываем продавцов с большим количеством товаров
        for saler in salers:
            if saler.count > 100:
                self.category_saler = [saler]
                self.page = saler.page
                return self.crawl()

        # Обрабатываем продавцов с малым количеством товаров
        small_salers = [saler for saler in salers if saler.count <= 100]
        grouped_salers = []
        current_group = []
        current_count = 0

        for saler in small_salers:
            if current_count + saler.count > 100:
                # Если добавление текущего продавца приведет к превышению 100 товаров, сохраняем текущую группу и начинаем новую
                grouped_salers.append(current_group)
                current_group = [saler]
                current_count = saler.count
            else:
                # Иначе добавляем текущего продавца в текущую группу
                current_group.append(saler)
                current_count += saler.count

        # Добавляем последнюю группу, если она не пуста
        if current_group:
            grouped_salers.append(current_group)

        # Теперь у нас есть группы продавцов, каждая из которых содержит до 100 товаров
        # Можно обработать каждую группу (например, вызвать 'self.crawl()' для каждой группы)
        for group in grouped_salers:
            self.category_saler = group
            self.page = 1
            return self.crawl()

    def crawl(self):
        fsupplier = ';'.join([str(saler.wb_id) for saler in self.category_saler])
        page = self.category_saler[0].page
        print('crawl fsupplier, page', fsupplier, page)
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog'
            f'?appType=1&curr=rub&dest=-1257786&page={page}&'
            f'fsupplier={fsupplier}&'
            f'&sort=popular&spp=0&'
            f'{self.category.wb_query}'
        )
        response = self.get_url(url)
        print('crawl response.status_code', response.status_code)
        if response.status_code == 200:
            if response.text == '':
                print('get_category')
                self.category_saler[0].delete()
                return self.get_category_salers()
            try:
                data = json.loads(r"{}".format(response.text))
                self.parse_catalog(data)
                self.page += 1
                self.category_saler[0].page = self.page
                self.category_saler[0].save()
            except JSONDecodeError as e:
                print('JSONDecodeError', e, url)
            except Exception as e:
                print('except', str(e))
        elif response.status_code == 429:
            print('get_category')
            sleep(10)
            return self.get_category_salers()
        else:
            return self.get_category_salers()

    def parse_catalog(self, data):
        print('parse_catalog', self.category.name, self.page)
        if len(data.get('data', {}).get('products', [])) > 0:
            self.parse_products(data['data']['products'])
            self.category.last_parsed_page = self.page
            self.category.last_parsed_page_at = datetime.now(timezone.utc)
            self.category.save()
        else:
            for saler in self.category_saler:
                saler.delete()

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
        else:
            self.notify('Ошибка получения складов. Статус: ', 
                        response.status_code)

    def get_url(self, url):
        sleep(TIMEOUT)
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
        thread = threading.Thread(target=self.update_products)
        thread.start()
        if self.config.parsing_done is not True:
            self.notify('Парсинг категорий начался')
            # self.get_wirehouses()
            self.get_category()
        # elif self.config.queries_done is not True:
        #     self.notify('Создаются поисковые запросы')
        #     self.create_queries()
        # elif self.config.queries_calculated is not True:
        #     self.notify('Расчет запросов начался')
        #     self.calculate_queries()
        elif self.config.categories_calculated is not True:
            self.notify('Расчет категорий начался')
            self.calculate_categories()
        # elif self.config.products_calculated is not True:
        #     self.notify('Расчет топ товаров начался')
        #     self.calculate_products()
        else:
            self.config.calculated = True
            self.config.save()
            thread_id = self.config.thread_id
            self.config = Config(
                thread_id=thread_id,
                current_parsing_id=int(
                    datetime.now(timezone.utc).timestamp()),
            )
            self.config.save()
            self.notify('Новый цикл начался')
            self.get_categories()
            Category.objects.update(
                calculated=False,
            )
            self.processing()

    def create_queries(self):
        categories = Category.objects.filter(parse=True)
        for category in categories:
            self.category = category
            product_ids = Product.objects.filter(
                categories__contains=[self.category.wb_id]
            ).exclude(root=None).values_list('id', flat=True)
            for sort in ['-profit_30_fbo', '-profit_30_fbo_grow']:
                pstats = ProductStat.objects.select_related('product').filter(
                    parsing_id=self.config.current_parsing_id,
                    product_id__in=product_ids).order_by(sort)[0:100]
                for pstat in pstats:
                    product = pstat.product
                    features = product.features
                    features.sort()
                    q = Query.objects.filter(
                        root=product.root,
                        features=features,
                        parsing_id=self.config.current_parsing_id
                    ).first()
                    if q is None:
                        q = Query(
                            root=product.root,
                            features=features,
                            parsing_id=self.config.current_parsing_id,
                            category_id=category.id,
                            first_product=product,
                        )
                        q.save()
                        print(q.root, q.features)
        self.config.queries_done = True
        self.config.save()
        self.processing()

    def update_category(self, child, i):
        category = Category.objects.filter(wb_id=child['id']).first()
        if category is None:
            category = Category(wb_id=child['id'])
        category.name = child.get('name')
        category.idx = i
        category.wb_query = child.get('query')
        category.parent = child.get('parent')
        category.seo = child.get('seo')
        category.url = child.get('url')
        category.shard = child.get('shard')
        category.parse = child.get('childs') is None
        category.save()
        for j, subchild in enumerate(child.get('childs', [])):
            self.update_category(subchild, j)
            # if subchild.get('shard') == 'blackhole':
            #     for subchild in child.get('childs', []):
            #         self.update_category(subchild)

    def get_categories(self):
        self.upgrade_parsing()
        # f = open('catalog.txt', 'r')
        # content = f.read()
        # categoryUrlList = [line for line in content.strip().split('\n')]
        # if '/catalog/' in line]
        # url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
        url = 'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
        response = self.get_url(url)
        data = response.json()
        stopCategories = ['Цифровые товары', 'Акции', 'Народные промыслы', 
                          'Путешествия']
        # for item in [item for item in data if item['name'] in categoryUrlList]:
        for i, item in enumerate(data):
            if item['name'] in stopCategories:
                continue
            self.update_category(item, i)
        self.notify('Категории обновлены')

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

    def get_category_old(self):
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
            Category.objects.exclude(parse=True).update(calculated=False)
            self.config.parsing_done = True
            self.config.save()
            # self.create_queries()
            # return self.calculate_query()
            return self.processing()
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

    def crawl_old(self):
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog'
            f'?appType=1&curr=rub&dest=-1257786&page={self.page}&'
            f'TestGroup=mmr_14&TestID=388&sort=popular&spp=0&{self.category.wb_query}'
        )
        # url = (
        #     f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog?'
        #     f'appType=1&couponsGeo={self.couponsGeo}&curr=rub&'
        #     f'dest={self.dest}&emp=0&lang=ru&locale=ru&'
        #     f'pricemarginCoeff=1.0&reg=1&regions={self.regions}&'
        #     f'sort=popular&spp=25&page={self.page}&{self.category.wb_query}'
        # )
        response = self.get_url(url)
        print('crawl response.status_code', response.status_code)
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
        elif response.status_code == 429:
            print('change_category')
            sleep(10)
            return self.change_category()
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
        return self.get_category()

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

    def update_products(self):
        product = Product.objects.filter(lemmas=[]).first()
        while product:
            self.text_process(product)
            # print('product.lemmas', product.lemmas)
            if len(product.lemmas) == 0:
                product.lemmas = ['-']
            product.save()
            product = Product.objects.filter(lemmas=[]).first()

    def get_keys(self, query):
        query = re.sub(r'[\W]', ' ', query)
        query = re.sub(r'\s+', ' ', query)
        doc = nlp(query.strip())
        lemmas = [w.lemma_ for w in doc if w.tag_ in 
                  ['ADV', 'ADJ', 'NOUN', 'VERB', 'NUM', 'INFN', 'PROPN', 'X', 'NUM']]
        features = list(set([w for w in doc if morph.parse(w.lemma_)[0].tag.POS == 'ADJF' or w.tag_ == 'ADJ']))
        doc = [t for t in doc if t not in features]
        root = [
            w for w in doc if (
                (
                    morph.parse(w.lemma_)[0].tag.POS == 'NOUN' or 
                    w.dep_ == 'ROOT' or 
                    w.tag_ == 'NOUN'
                ) and len(w.lemma_) > 2
            )
        ]
        return root[0].lemma_ if len(root) else None, [f.lemma_ for f in features], lemmas

    def text_process(self, product):
        root, features, lemmas = self.get_keys(product.name)
        product.root = root or '-'
        product.features = features
        product.lemmas = lemmas
        # if len(doc.ents):
        #     product.entity = doc.ents[0].lemma_

    def check_unique(self, product):
        print(product.articul)
        Product.objects.filter(articul=product.articul).exclude(
            id=product.id).delete()
        product.check_articul = True
        product.save()

    def product_calculate(self, product, pstat):
        start = (datetime.now(timezone.utc) - timedelta(days=30)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        last_stats = product.productstat_set.filter(
            date__gte=start).values()
        update = {}
        for fb in ['fbo', 'fbs']:
            sales_zero_count = len([s for s in last_stats 
                                    if s[f'sales_{fb}'] == 0])
            sales = [s[f'sales_{fb}'] for s in last_stats if s[f'sales_{fb}'] > 0]
            if len(sales):
                sales_avg = sum(sales) / len(sales)
                update[f'profit_lost_{fb}'] = sales_zero_count * sales_avg
        for period in [7, 14, 30]:
            start_period = (datetime.now(timezone.utc) - timedelta(
                days=period)).replace(hour=0, minute=0, second=0, 
                                      microsecond=0)
            data = [stat for stat in last_stats 
                    if stat['date'] >= start_period]
            for fb in ['fbo', 'fbs']:
                sales = sum([stat[f'sales_{fb}'] for stat in data])
                profit = sum([stat[f'sales_{fb}'] * stat['price'] 
                              for stat in data])
                update[f'sales_{period}_{fb}'] = sales
                update[f'profit_{period}_{fb}'] = profit
        if last_stats.count() > 1:
            if last_stats[1]['profit_30_fbo'] > 0:
                update['profit_30_fbo_grow'] = last_stats[0]['profit_30_fbo'] / last_stats[1]['profit_30_fbo']
        product.productstat_set.filter(pk=pstat.id).update(**update)

    def parse_products(self, products):
        ids = [p['id'] for p in products]
        details = self.get_details(ids)
        for index, item in enumerate(products):
            name = item.get('name', '').strip()
            if name == '':
                continue
            price = item.get('salePriceU') / 100
            priceU = item.get('priceU') / 100
            detail = [detail for detail in details if detail['id'] == item['id']]
            if len(detail):
                detail = detail[0]
                sizes = detail.get('sizes', [])
                quantity_fbo = 0
                quantity_fbs = 0
                for size in sizes:
                    for stock in size.get('stocks', []):
                        qty = stock.get('qty', 0)
                        if stock.get('wh') in self.wirehouses:
                            quantity_fbo += qty
                        else:
                            quantity_fbs += qty
            else:
                continue
            product = Product.objects.filter(articul=item['id']).first()
            if product:
                if product.name != name:
                    product.name = name
                self.text_process(product)
                product.name = name
                product.supplier_id = item['supplierId']
                product.brand = item['brand']
                product.brand_id = item['siteBrandId']
                product.rating = item['rating']
                product.feedbacks = item['feedbacks']
                product.price = price
                product.priceU = priceU
                product.parsed_at = datetime.now(timezone.utc)
                product.updated_at = datetime.now(timezone.utc)
                if self.query is None and self.category.wb_id not in product.categories:
                    product.categories.append(self.category.wb_id)
                sales_fbo = 0
                sales_fbs = 0
                last_stat = product.productstat_set.first()
                if last_stat is None or (last_stat.parsing_id != self.config.current_parsing_id):
                    # Если последняя цена вчерашняя то посчитать
                    # разницу остатков и записать как количество продаж
                    # sales = product.quantity - quantity
                    if last_stat and last_stat.quantity_fbo is not None:
                        sales_fbo = last_stat.quantity_fbo - quantity_fbo
                    if last_stat and last_stat.quantity_fbs is not None:
                        sales_fbs = last_stat.quantity_fbs - quantity_fbs
                    # если цифра отрицательная то вероятно поступление
                    # на склад и расчет не получится
                    # if sales < 0:
                    #     sales = 0
                    if sales_fbo < 0:
                        sales_fbo = 0
                    if sales_fbs < 0:
                        sales_fbs = 0
                    pstat = product.productstat_set.create(
                        parsing_id=self.config.current_parsing_id,
                        sales_fbo=sales_fbo,
                        sales_fbs=sales_fbs,
                        price=price,
                        priceU=priceU,
                        profit_fbo=sales_fbo * price,
                        profit_fbs=sales_fbs * price,
                        quantity_fbo=quantity_fbo,
                        quantity_fbs=quantity_fbs,
                        date=datetime.now(timezone.utc)
                    )
                    self.product_calculate(product, pstat)
                product.save()
            else:
                product = Product(
                    articul=item['id'],
                    name=name,
                    supplier_id=item['supplierId'],
                    brand=item['brand'],
                    brand_id=item['siteBrandId'],
                    categories=[self.category.wb_id],
                    rating=item['rating'],
                    feedbacks=item['feedbacks'],
                    priceU=priceU,
                    price=price,
                    parsed_at=datetime.now(timezone.utc),
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                self.text_process(product)
                product.save()
                product.productstat_set.create(
                    parsing_id=self.config.current_parsing_id,
                    quantity_fbo=quantity_fbo,
                    quantity_fbs=quantity_fbs,
                    price=price,
                    priceU=priceU,
                    date=datetime.now(timezone.utc)
                )

    def parse_search(self, data):
        print('parse_search', self.query)
        if len(data.get('data', {}).get('products', [])):
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

    def parse_catalog_old(self, data):
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
        # отправляются в раздел ""топ категории""
        def get_child_ids(category):
            ids = [category.wb_id]
            for child in Category.objects.filter(parent=category.wb_id):
                ids.append(child.wb_id)
                ids += get_child_ids(child)
            return ids
        update = {}
        wb_ids = get_child_ids(category)
        products = Product.objects.filter(categories__overlap=wb_ids)
        product_ids = products.values_list('id', flat=True)
        update['products_count'] = product_ids.count()
        print('calculate_category', update)
        if update['products_count'] == 0:
            category.calculated = True
            category.save()
            return
        productstats_current = ProductStat.objects.filter(
            parsing_id=self.config.current_parsing_id,
            product_id__in=product_ids
        )
        if productstats_current.count() < 10:
            category.calculated = True
            category.save()
            return
        last_agg = productstats_current.aggregate(
            sold_7_fbo=Count('sales_7_fbo', filter=Q(sales_7_fbo__gt=0)),
            sold_14_fbo=Count('sales_14_fbo', filter=Q(sales_14_fbo__gt=0)),
            sold_30_fbo=Count('sales_30_fbo', filter=Q(sales_30_fbo__gt=0)),
            sold_7_fbs=Count('sales_7_fbs', filter=Q(sales_7_fbs__gt=0)),
            sold_14_fbs=Count('sales_14_fbs', filter=Q(sales_14_fbs__gt=0)),
            sold_30_fbs=Count('sales_30_fbs', filter=Q(sales_30_fbs__gt=0)),
            sellers_solded_7_fbo=Count('product__supplier_id', filter=Q(
                sales_7_fbo__gt=0), distinct=True),
            sellers_solded_7_fbs=Count('product__supplier_id', filter=Q(
                sales_7_fbs__gt=0), distinct=True),
            sellers_solded_14_fbo=Count('product__supplier_id', filter=Q(
                sales_14_fbo__gt=0), distinct=True),
            sellers_solded_14_fbs=Count('product__supplier_id', filter=Q(
                sales_14_fbs__gt=0), distinct=True),
            sellers_solded_30_fbo=Count('product__supplier_id', filter=Q(
                sales_30_fbo__gt=0), distinct=True),
            sellers_solded_30_fbs=Count('product__supplier_id', filter=Q(
                sales_30_fbs__gt=0), distinct=True),
        )
        update['products_solded_7_fbo'] = last_agg['sold_7_fbo']  # / len(product_ids) * 100
        update['products_solded_7_fbs'] = last_agg['sold_7_fbs']  # / len(product_ids) * 100
        update['products_solded_14_fbo'] = last_agg['sold_14_fbo']  # / len(product_ids) * 100
        update['products_solded_14_fbs'] = last_agg['sold_14_fbs']  # / len(product_ids) * 100
        update['products_solded_30_fbo'] = last_agg['sold_30_fbo']  # / len(product_ids) * 100
        update['products_solded_30_fbs'] = last_agg['sold_30_fbs']  # / len(product_ids) * 100
        update['sellers_solded_7_fbo'] = last_agg['sellers_solded_7_fbo']
        update['sellers_solded_7_fbs'] = last_agg['sellers_solded_7_fbs']
        update['sellers_solded_14_fbo'] = last_agg['sellers_solded_14_fbo']
        update['sellers_solded_14_fbs'] = last_agg['sellers_solded_14_fbs']
        update['sellers_solded_30_fbo'] = last_agg['sellers_solded_30_fbo']
        update['sellers_solded_30_fbs'] = last_agg['sellers_solded_30_fbs']
        print('---')
        print(update)
        print('---')
        for period in [7, 14, 30]:
            print('period', period)
            start = (datetime.now() - timedelta(days=period)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            parsing_ids = Config.objects.filter(
                current_parsing_id__gte=start.timestamp()
            ).values_list('current_parsing_id', flat=True)
            if len(parsing_ids) == 0:
                continue
            productstats = ProductStat.objects.select_related('product').filter(
                parsing_id__in=parsing_ids,
                product_id__in=product_ids
            )
            agg = productstats.aggregate(
                Avg('price'),
                Sum('profit_fbo'),
                Sum('profit_fbs'),
                sellers=Count('product__supplier_id', distinct=True),
            )
            print('agg', agg)
            update[f'price_avg_{period}'] = agg['price__avg']
            update[f'profit_{period}_fbo'] = agg['profit_fbo__sum']
            update[f'profit_{period}_fbs'] = agg['profit_fbs__sum']
            update[f'sellers_count_{period}'] = agg['sellers']
            # if update['products_count'] > 300:
            #     continue
            # prev_parsing = Config.objects.filter(
            #     current_parsing_id__lt=start.timestamp()).first()
            # prev_stat = CategoryStat.objects.filter(
            #     category_id=category.id,
            #     parsing_id=prev_parsing.current_parsing_id).first()
            for fb in ['fbo', 'fbs']:
                field = f'profit_{period}_{fb}'
                pstats = productstats_current.order_by(f'-{field}')[:10].values()

                # Средний чек от 750 рублей
                if (update[f'price_avg_{period}'] or 0) < 750:
                    continue
                # Количество товаров с продажами от 25%
                if update[f'products_solded_{period}_{fb}'] < 25:
                    continue
                # Оборот в категории от 20 млн
                if update.get(field, 0) < 20000000:
                    continue
                # Монополия: меньше 30%
                top_10_profit = sum([stat.get(field, 0) for stat in pstats])
                if top_10_profit / update.get(field, 1) > 0.3:
                    continue
                update[f'top_{period}_{fb}'] = True
                # # - Оборот первого товара не меньше 500к
                # if pstats.count() == 0:
                #     continue
                # if pstats[0][field] < self.profit_first_top / 30 * period:
                #     continue
                # # оборот десятого товара не меньше 100к
                # if pstats[9][field] < self.profit_ten_top / 30 * period:
                #     continue
                # # - Количество товаров с продажами: не меньше 20%
                # if update[f'products_solded_{period}_{fb}'] < 20:
                #     continue
                # # - Оборот в категории месяц назад и сейчас отличается не более чем на +-10%
                # if prev_stat is None:
                #     continue
                # _prev_stat = model_to_dict(prev_stat)
                # if _prev_stat[field] is None or update[field] < _prev_stat[field] * 0.9:
                #     continue
                # if _prev_stat[field] is None or update[field] > _prev_stat[field] * 1.1:
                #     continue
                # # - Средний чек в категории месяц назад и сейчас отличается не более чем на +-10%
                # if _prev_stat[f'price_avg_{period}'] is None or update[f'price_avg_{period}'] < _prev_stat[f'price_avg_{period}'] * 0.9:
                #     continue
                # if _prev_stat[f'price_avg_{period}'] is None or update[f'price_avg_{period}'] > _prev_stat[f'price_avg_{period}'] * 1.1:
                #     continue
        stat = category.categorystat_set.filter(
            parsing_id=self.config.current_parsing_id).first()
        if stat is None:
            stat = category.categorystat_set.create(
                parsing_id=self.config.current_parsing_id)
        CategoryStat.objects.filter(pk=stat.id).update(**update)
        update['scoring'] = get_scoring_productstats(product_ids, self.config)
        print('update scoring', stat.id, update['scoring'])
        CategoryStat.objects.filter(pk=stat.id).update(**update)
        first_product = Product.objects.filter(
            categories__overlap=[category.wb_id]).first()
        if first_product:
            category.first_product = first_product
        category.calculated = True
        category.save()

    def calculate_queries(self):
        query = Query.objects.filter(
            parsing_id=self.config.current_parsing_id,
        ).exclude(calculated=True).first()
        while query:
            self.calculate_query_v2(query)
            query = Query.objects.filter(
                parsing_id=self.config.current_parsing_id,
            ).exclude(calculated=True).first()
        self.config.queries_calculated = True
        self.config.save()
        self.processing()

    def update_parsed_parent(self, category, parent):
        if category.id not in parent.parsed_ids:
            parent.parsed_ids.append(category.wb_id)
            parent.save()
        parent = Category.objects.filter(wb_id=parent.parent).first()
        if parent:
            self.update_parsed_parent(category, parent)

    def update_category_tree(self):
        Category.objects.all().update(parsed_ids=[])
        for category in Category.objects.filter(parse=True):
            parent = Category.objects.filter(wb_id=category.parent).first()
            if parent:
                print(parent.name, category.name)
                self.update_parsed_parent(category, parent)

    def calculate_categories(self):
        category = Category.objects.exclude(
            calculated=True).first()
        while category:
            self.calculate_category(category)
            category = Category.objects.exclude(
                calculated=True).first()
        self.config.categories_calculated = True
        self.config.save()
        self.processing()

    def calculate_query_products(self):
        pass

    def calculate_query(self, query):
        update = {}
        product_ids = list(Product.objects.filter(
            root=query.root, features__contains=query.features
        ).values_list('id', flat=True))
        update['products_count'] = len(product_ids)
        if update['products_count'] == 0:
            query.delete()
            return
        
        productstats_current = ProductStat.objects.filter(
            parsing_id=self.config.current_parsing_id,
            product_id__in=product_ids
        )
        last_agg_values = list(productstats_current.values(
            'sales_7_fbo', 'sales_14_fbo', 'sales_30_fbo', 
            'sales_7_fbs', 'sales_14_fbs', 'sales_30_fbs'))
        last_agg = {
            'sold_7_fbo': 0,
            'sold_7_fbs': 0,
            'sold_14_fbo': 0,
            'sold_14_fbs': 0,
            'sold_30_fbo': 0,
            'sold_30_fbs': 0,
        }
        for value in last_agg_values:
            for fb in ['fbo', 'fbs']:
                for period in [7, 14, 30]:
                    if value[f'sales_{period}_{fb}'] > 0:
                        last_agg[f'sold_{period}_{fb}'] += 1

        update['products_solded_7_fbo'] = last_agg['sold_7_fbo'] / len(product_ids) * 100
        update['products_solded_7_fbs'] = last_agg['sold_7_fbs'] / len(product_ids) * 100
        update['products_solded_14_fbo'] = last_agg['sold_14_fbo'] / len(product_ids) * 100
        update['products_solded_14_fbs'] = last_agg['sold_14_fbs'] / len(product_ids) * 100
        update['products_solded_30_fbo'] = last_agg['sold_30_fbo'] / len(product_ids) * 100
        update['products_solded_30_fbs'] = last_agg['sold_30_fbs'] / len(product_ids) * 100

        productstats_current_count = productstats_current.count()
        if productstats_current_count < 11 or productstats_current_count > 2500:
            query.delete()
            return
        deleteQuery = True
        for period in [7, 14, 30]:
            start = (datetime.now() - timedelta(days=period)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            parsing_ids = Config.objects.filter(
                current_parsing_id__gte=start.timestamp()
            ).values_list('current_parsing_id', flat=True)
            if len(parsing_ids) == 0:
                continue
            productstats = ProductStat.objects.filter(
                parsing_id__in=parsing_ids,
                product_id__in=product_ids
            )
            agg = productstats.aggregate(
                Avg('price'),
                Sum('profit_fbo'),
                Sum('profit_fbs'),
            )
            update[f'price_avg_{period}'] = agg['price__avg']
            update[f'profit_{period}_fbo'] = agg['profit_fbo__sum']
            update[f'profit_{period}_fbs'] = agg['profit_fbs__sum']
            start_prev = start - timedelta(days=period)
            parsing_ids_prev = Config.objects.filter(
                current_parsing_id__gte=start_prev.timestamp(),
                current_parsing_id__lt=start.timestamp(),
            ).values_list('current_parsing_id', flat=True)
            productstats_prev = ProductStat.objects.filter(
                parsing_id__in=parsing_ids_prev,
                product_id__in=product_ids
            )
            agg_prev = productstats_prev.aggregate(
                Avg('price'),
                Sum('profit_fbo'),
                Sum('profit_fbs'),
            )
            for fb in ['fbo', 'fbs']:
                field = f'profit_{period}_{fb}'
                pstats = list(productstats_current.order_by(f'-{field}')[:10].values())
                if len(pstats) < 10:
                    continue
                update[f'product_1_{field}'] = pstats[0][field]
                update[f'product_10_{field}'] = pstats[9][field]
                # Оборот первого не меньше 300к в месяц
                if update[f'product_1_{field}'] < 300000 * period / 30:
                    continue
                # оборот десятого не меньше 70к в месяц
                if update[f'product_10_{field}'] < 70000 * period / 30:
                    continue
                # Количество товаров с продажами: не меньше 20%
                if update[f'products_solded_{period}_{fb}'] < 20:
                    continue
                # Средний чек в категории месяц назад и сейчас
                # отличается не более чем на +/- 40%
                if update[f'price_avg_{period}'] < (agg_prev['price__avg'] or 0) * 0.6:
                    continue
                if update[f'price_avg_{period}'] > (agg_prev['price__avg'] or 0) * 1.4:
                    continue
                # Оборот в категории месяц назад и сейчас отличается
                # не более чем на +/- 10%
                if update[field] < agg_prev[f'profit_{fb}__sum'] * 0.9:
                    continue
                if update[field] > agg_prev[f'profit_{fb}__sum'] * 1.1:
                    continue
                update[f'top_{period}_{fb}'] = True
                deleteQuery = False
        print(deleteQuery, update)
        if deleteQuery:
            query.delete()
        else:
            update['calculated'] = True
            print('query calculated TOP', update)
            Query.objects.filter(pk=query.id).update(**update)

    def calculate_query_v2(self, query):
        update = {}
        product_ids = list(Product.objects.filter(
            root=query.root, features__contains=query.features
        ).values_list('id', flat=True))
        update['products_count'] = len(product_ids)
        if update['products_count'] == 0:
            query.delete()
            return
        period = 30
        start_30 = (datetime.now() - timedelta(days=period)).replace(
                hour=0, minute=0, second=0, microsecond=0)
        start_prev_30 = start_30 - timedelta(days=period)
        parsing_ids = Config.objects.filter(
            current_parsing_id__gte=start_prev_30.timestamp()
        ).values_list('current_parsing_id', flat=True)
        productstats = list(ProductStat.objects.filter(
            parsing_id__in=parsing_ids,
            product_id__in=product_ids
        ).values())

        productstats_current = [ps for ps in productstats if ps['parsing_id'] == self.config.current_parsing_id]

        last_agg = {
            'sold_7_fbo': 0,
            'sold_7_fbs': 0,
            'sold_14_fbo': 0,
            'sold_14_fbs': 0,
            'sold_30_fbo': 0,
            'sold_30_fbs': 0,
        }
        for value in productstats_current:
            for fb in ['fbo', 'fbs']:
                for period in [7, 14, 30]:
                    if value[f'sales_{period}_{fb}'] > 0:
                        last_agg[f'sold_{period}_{fb}'] += 1

        update['products_solded_7_fbo'] = last_agg['sold_7_fbo'] / len(product_ids) * 100
        update['products_solded_7_fbs'] = last_agg['sold_7_fbs'] / len(product_ids) * 100
        update['products_solded_14_fbo'] = last_agg['sold_14_fbo'] / len(product_ids) * 100
        update['products_solded_14_fbs'] = last_agg['sold_14_fbs'] / len(product_ids) * 100
        update['products_solded_30_fbo'] = last_agg['sold_30_fbo'] / len(product_ids) * 100
        update['products_solded_30_fbs'] = last_agg['sold_30_fbs'] / len(product_ids) * 100

        productstats_current_count = len(productstats_current)
        if productstats_current_count < 11 or productstats_current_count > 5000:
            query.delete()
            return
        deleteQuery = True
        for period in [7, 14, 30]:
            period_start = (datetime.now() - timedelta(days=period)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            # period_parsing_id = Config.objects.filter(
            #     current_parsing_id__gte=start.timestamp()
            # ).last().current_parsing_id
            # # ).values_list('current_parsing_id', flat=True)
            # # if len(period_parsing_ids) == 0:
            # #     continue
            # productstats_period = [ps for ps in productstats if ps['parsing_id'] == period_parsing_id]
            # if len(productstats_period) == 0:
            #     continue
            update[f'price_avg_{period}'] = int(sum([ps['price'] for ps in productstats_current]) / len(productstats_current))
            update[f'profit_{period}_fbo'] = int(sum([ps[f'profit_{period}_fbo'] for ps in productstats_current]))
            update[f'profit_{period}_fbs'] = int(sum([ps[f'profit_{period}_fbs'] for ps in productstats_current]))
            
            # prev_period_start = period_start - timedelta(days=period)
            period_start_parsing_id = Config.objects.filter(
                current_parsing_id__gte=period_start.timestamp(),
            ).last().current_parsing_id
            productstats_prev = [ps for ps in productstats if ps['parsing_id'] == period_start_parsing_id]
            if len(productstats_prev) == 0:
                continue
            productstats_prev_price_avg = int(sum([ps['price'] for ps in productstats_prev]) / len(productstats_prev))
            for fb in ['fbo', 'fbs']:
                field = f'profit_{period}_{fb}'
                pstats = sorted(productstats_current, key=lambda x: x[field], reverse=True)[:10]
                if len(pstats) < 10:
                    continue
                update[f'product_1_{field}'] = pstats[0][field]
                update[f'product_10_{field}'] = pstats[9][field]
                # Оборот первого не меньше 300к в месяц
                if update[f'product_1_{field}'] < 300000 * period / 30:
                    continue
                # оборот десятого не меньше 70к в месяц
                if update[f'product_10_{field}'] < 70000 * period / 30:
                    continue
                # Количество товаров с продажами: не меньше 20%
                if update[f'products_solded_{period}_{fb}'] < 20:
                    continue
                # Средний чек в категории месяц назад и сейчас
                # отличается не более чем на +/- 40%
                if update[f'price_avg_{period}'] < (productstats_prev_price_avg or 0) * 0.6:
                    continue
                if update[f'price_avg_{period}'] > (productstats_prev_price_avg or 0) * 1.4:
                    continue
                # Оборот в категории месяц назад и сейчас отличается
                # не более чем на +/- 10%
                profit_sum = int(sum([ps[f'profit_{period}_{fb}'] for ps in productstats_prev]))
                if update[field] < profit_sum * 0.9:
                    continue
                if update[field] > profit_sum * 1.1:
                    continue
                update[f'top_{period}_{fb}'] = True
                deleteQuery = False
        print(deleteQuery, update)
        if deleteQuery:
            query.delete()
        else:
            update['calculated'] = True
            print('query calculated TOP', query.id, update)
            Query.objects.filter(pk=query.id).update(**update)
            self.get_query_scoring(query.id)

    def get_query_scoring(self, query_id):
        # print('get_query_scoring', model_to_dict(query))
        query = Query.objects.get(pk=query_id)
        # date = datetime.now()
        # fb = 'fbo'
        config = self.config
        if query.first_product_id:
            product = Product.objects.get(pk=query.first_product_id)
            query_root, query_features = product.root, product.features
            # self.get_keys(product.name)
        else:
            query_root = query.root
            query_features = query.features
        product_ids = Product.objects.filter(
            root=query_root,
            features__contains=query_features
        ).values_list('id', flat=True)
        query.scoring = get_scoring_productstats(product_ids, config)
        query.save()

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

