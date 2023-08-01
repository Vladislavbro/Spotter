import requests
from django.db.models import Sum, Avg, Q, Count
from api.models import Product, Supplier
from datetime import datetime, timedelta, timezone
import sys
from api.proxies import proxies
from random import choice
from random_user_agent.user_agent import UserAgent
import os
import pytz


utc = pytz.UTC
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
# nlp = spacy.load('ru_core_news_md')

user_agent_rotator = UserAgent()
# TOKEN = '6161677884:AAE8uT0XWRVXr7SbGIjVTP3Ik6BhsDm8Z5I'
# bot = Bot(token=TOKEN)

sys.setrecursionlimit(10**6)


class Basket(object):
    """docstring for Basket."""
    product = None
    baskets = []

    def __init__(self):
        super(Basket, self).__init__()
        self.baskets = list(Product.objects.filter(basket__gt=0).values('basket').annotate(Count('id')).order_by('-id__count').values_list('basket', flat=True))
        print('baskets', self.baskets)
        self.get_basket()

    def get_basket(self):
        self.product = Product.objects.filter(basket=None).first()
        while self.product:
            articul = self.product.articul
            # baskets = ['10', '05', '04', '03', '02', '09', '01', '08', '06', '07', '11', '12']
            for basket in self.baskets:
                if basket < 10:
                    basket = f'0{basket}'
                else:
                    basket = str(basket)
                url = 'https://basket-' + basket + '.wb.ru/vol' + str(articul)[:-5] + '/part'
                url += str(articul)[:-3] + '/' + str(articul) + '/info/sellers.json'
                headers = {
                    'User-Agent': user_agent_rotator.get_random_user_agent()
                }
                proxy = choice(proxies)
                response = requests.get(url, headers=headers, proxies={
                    'http': proxy,
                    'https': proxy,
                })
                # {
                #     "nmId": 138098499,
                #     "supplierId": 975054,
                #     "supplierName": "ИП Клепиков А. Ю.",
                #     "inn": "772019882755",
                #     "ogrn": "322774600471670",
                #     "ogrnip": "322774600471670",
                #     "trademark": "Klepiks",
                #     "rv": 12636635372
                # }
                if response.status_code == 200:
                    data = response.json()
                    self.product.basket = int(basket)
                    if (data.get('supplierId') and 
                            not Supplier.objects.filter(
                                wb_id=data.get('supplierId')).exists()):
                        Supplier.objects.create(
                            wb_id=data['supplierId'],
                            name=data['supplierName'],
                            inn=data.get('inn'),
                            ogrn=data.get('ogrn'),
                            ogrnip=data.get('ogrnip'),
                            trademark=data.get('trademark'),
                        )
                    break
            if not self.product.basket:
                self.product.basket = 0
            print('product.basket', self.product.basket)
            self.product.save()
            self.product = Product.objects.filter(basket=None).first()