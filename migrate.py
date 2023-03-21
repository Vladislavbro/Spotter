from models import Categories, Products, Config, Queries
import requests
import json


class Migrate(object):
    """docstring for Migrate."""

    def __init__(self):
        super(Migrate, self).__init__()
        self.transfer_products()

    def transfer_configs(self):
        for config in Config.objects.all():
            response = requests.post(
                'http://localhost:8000/api/transfer/config',
                json=config.to_json()
            )
            print(response.status_code)
            if response.status_code == 200:
                print('response.text', response.text)
                config.pg_id = int(response.text)
                config.save()
            else:
                print('xz')

    def transfer_categories(self):
        for category in Categories.objects.all():
            response = requests.post(
                'http://localhost:8000/api/transfer/category',
                json=category.to_json()
            )
            print(response.status_code)
            if response.status_code == 200:
                print('response.text', response.text)
                category.pg_id = int(response.text)
                category.save()
            else:
                print('xz')

    def transfer_queries(self):
        for query in Queries.objects.all():
            response = requests.post(
                'http://localhost:8000/api/transfer/query',
                json=query.to_json()
            )
            print(response.status_code)
            if response.status_code == 200:
                print('response.text', response.text)
                query.pg_id = int(response.text)
                query.save()
            else:
                print('xz')

    def transfer_products(self):
        print('transfer_products')
        product = Products.objects.filter(pg_id=None).first()
        print('product', product)
        while product:
            response = requests.post(
                'http://localhost:8000/api/transfer/product',
                json=product.to_json()
            )
            print(response.status_code)
            if response.status_code == 200:
                print('response.text', response.text)
                product.pg_id = int(response.text)
                product.save()
            else:
                print('xz')
            product = Products.objects.filter(pg_id=None).first()


Migrate()
