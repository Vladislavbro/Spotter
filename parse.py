import requests
from models import Categories, Products
from time import sleep
from datetime import datetime
import time
import sys
from telegram import Bot
import sys, traceback
from json import JSONDecodeError

TOKEN = '507933514:AAHP_BHtTUEES3Mq9giC231W4ZkvfeqSBb0'
bot = Bot(token=TOKEN)
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    ),
}

sys.setrecursionlimit(10**6)


class Parser(object):
    """docstring for Parser."""
    regions = '68,64,83,4,38,80,33,70,82,86,75,30,69,1,48,22,66,31,40,71'
    dest = '-1029256,-102269,-2162196,-1257786'
    couponsGeo = '12,3,18,15,21'
    page = 1
    category = None
    adminIds = [259180458]
    expandCategories = [
        'Гостиная',
        'Кухня',
        'Досуг и творчество',
        'Сумки и рюкзаки',
        'Мебельная фурнитура',
        'Краски и грунтовки',
        'Одежда для девочек',
        'Одежда для мальчиков',
        'Школьные принадлежности',
    ]

    def __init__(self):
        super(Parser, self).__init__()
        self.get_category()

    def create_category(self, child):
        if Categories.objects(wb_id=child['id']).first() is None:
            category = Categories(
                name=child['name'],
                wb_id=child['id'],
                parent=child['parent'],
                query=child.get('query'),
                seo=child.get('seo'),
                url=child['url'],
                shard=child.get('shard'),
            )
            category.save()

    def get_categories(self):
        f = open('catalog.txt', 'r')
        content = f.read()
        categoryUrlList = [line for line in content.strip().split('\n')
                           if '/catalog/' in line]
        url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
        response = requests.get(url, headers=headers)
        data = response.json()
        for item in data:
            # print(item['name'])
            for child in item.get('childs', []):
                # print(child['url'])
                if child['url'] in categoryUrlList:
                    if child['name'] in self.expandCategories:
                        print('expandCategories', child['id'])
                        for subchild in child.get('childs', []):
                            self.create_category(subchild)
                    else:
                        if child['url'] == '/catalog/dlya-remonta/krepezh/mebelnaya-furnitura':
                            child['query'] = 'subject=2361;2893;3817;4263;5059;5176;5975;6341;7308;7349;7350;7351;7353;7354;7355;7356;7357;7564'
                        self.create_category(child)

    def notify(self, text):
        for id in self.adminIds:
            try:
                bot.send_message(chat_id=id, text=text)
            except:
                print('send message except')

    def get_category(self):
        self.category = Categories.objects.filter(parsed_at=None).first()
        if self.category is None:
            self.notify('Парсинг категорий закончился')
            Categories.objects.all().update(
                parsed_at=None,
                last_parsed_page=None,
                last_parsed_page_at=None,
            )
            return self.caclulate()
        else:
            if self.category.last_parsed_page:
                self.page = self.category.last_parsed_page + 1
            else:
                self.category.start_parsing_at = datetime.utcnow()
                self.category.current_parsing_id = int(time.time())
                self.category.save()
                self.page = 1
            return self.crawl()

    def crawl(self):
        url = (
            f'https://catalog.wb.ru/catalog/{self.category.shard}/catalog?'
            f'appType=1&couponsGeo={self.couponsGeo}&curr=rub&'
            f'dest={self.dest}&emp=0&lang=ru&locale=ru&'
            f'pricemarginCoeff=1.0&reg=1&regions={self.regions}&'
            f'sort=popular&spp=25&page={self.page}&{self.category.query}'
        )
        print(self.category.name, self.page)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if response.text == '':
                return self.change_category()
            try:
                data = response.json()
                self.parse_catalog(data)
            except JSONDecodeError as e:
                print('JSONDecodeError', e, response)
            except Exception as e:
                print('except', str(e))

    def change_category(self):
        self.category.last_parsed_page_at = datetime.utcnow()
        self.category.parsed_at = datetime.utcnow()
        self.category.save()
        self.get_category()

    def parse_catalog(self, data):
        print('parse_catalog', self.category.name, self.page)
        if len(data.get('data', {}).get('products', [])) > 0:
            print('products:', len(data['data']['products']))
            for index, item in enumerate(data['data']['products']):
                product = Products.objects(
                    articul=item['id']
                ).fields(slice__sizes=[-2, 2]).first()
                price = item.get('salePriceU') / 100
                sizes = item.get('sizes', [])
                quantity = sum([size['rank'] for size in sizes])
                sales = 0
                if len(product.sizes):
                    # Проверить что последняя запись вчерашняя
                    if product.sizes[-1].date.day != datetime.utcnow().day:
                        # Если вчерашняя то посчитать разницу остатков и
                        # записать как количество продаж
                        sales = product.quantity - quantity
                        # если цифра отрицательная то вероятно поступление
                        # на склад и расчет не получится
                        if sales < 0:
                            sales = 0

                if product:
                    Products.objects(id=product.id).update_one(
                        set__last_parsing_id=self.category.current_parsing_id,
                        set__name=item['name'],
                        set__brand=item['brand'],
                        set__brand_id=item['siteBrandId'],
                        set__category_name=self.category.name,
                        set__category_id=self.category.id,
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
                    if len(product.sizes) and product.sizes[-1].date.day == datetime.utcnow().day:
                        pass
                    else:
                        Products.objects(id=product.id).update_one(
                            push__sizes={
                                'quantity': quantity,
                                'date': datetime.utcnow()
                            }
                        )
                else:
                    product = Products(
                        articul=item['id'],
                        name=item['name'],
                        brand=item['brand'],
                        brand_id=item['siteBrandId'],
                        category_name=self.category.name,
                        category_id=self.category.id,
                        subject_id=item['subjectId'],
                        rating=item['rating'],
                        feedbacks=item['feedbacks'],
                        is_new=item.get('isNew', False),
                        data=item,
                        price=price,
                        priceU=(item.get('priceU') / 100),
                        quantity=quantity,
                        last_parsing_id=self.category.current_parsing_id,
                        parsed_at=datetime.utcnow(),
                    )
                    product.sizes.create(quantity=quantity,
                                         date=datetime.utcnow())
                    product.save()

            self.category.last_parsed_page = self.page
            self.category.last_parsed_page_at = datetime.utcnow()
            self.category.save()
            self.page += 1

            sleep(0.2)

            if self.page > 100:
                self.change_category()
            else:
                self.get_category()
        else:
            self.change_category()

    def caclulate(self):
        self.notify('Расчёт начался')


parser = Parser()
