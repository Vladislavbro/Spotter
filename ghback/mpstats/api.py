import requests
from .models import Category


class Mpstats:
    headers = {
        'X-Mpstats-TOKEN': '65d78fba6d7824.982500042ed2ade776ce4f181ede657c3afab330',
        'Content-Type': 'application/json',
    }

    def __init__(self):
        pass

    def get_subjects(self):
        url = f"https://mpstats.io/api/wb/get/subjects/select"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        for item in data:
            print(item['name'])

    def get_subcategories(self, path):
        url = f"https://mpstats.io/api/wb/get/category/items?path={path}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        for item in data:
            print(item['name'])

    def get_categories_stat(self):
        for root in Category.objects.filter(parent=None):
            print(root.name)
            url = f"https://mpstats.io/api/wb/get/category/items?path={root.path}"
            response = requests.get(url, headers=self.headers)
            data = response.json()
            for item in data:
                category = Category.objects.get(name=item['name'])
                if category is None:
                    continue
                category.sales = item['sales']
                category.revenue = item['revenue']
                category.items = item['items']
                category.items_with_sells = item['items_with_sells']
                category.items_with_sells_percent = item['items_with_sells_percent']
                category.sellers = item['sellers']
                category.sellers_with_sells = item['sellers_with_sells']
                category.brands = item['brands']
                category.brands_with_sells = item['brands_with_sells']
                category.sellers_with_sells_percent = item['sellers_with_sells_percent']
                category.sales_per_items_average = item['sales_per_items_average']
                category.revenue_per_items_average = item['revenue_per_items_average']
                category.avg_price = item['avg_price']
                category.median_price = item['median_price']
                category.rating = item['rating']
                category.comments = item['comments']
                category.balance = item['balance']
                category.live_items = item['live_items']
                category.revenue_potential = item['revenue_potential']
                category.lost_profit = item['lost_profit']
                category.lost_profit_percent = item['lost_profit_percent']
                category.graph = item['graph']
                category.commision_fbo = item['commision_fbo']
                category.commision_fbs = item['commision_fbs']
                category.basic_logistics = item['basic_logistics']
                category.storage_price = item['storage_price']
                category.acceptance_price = item['acceptance_price']
                category.delivery_by_volume = item['delivery_by_volume']
                category.purchase = item['purchase']
                category.purchase_after_return = item['purchase_after_return']
                category.save()

    def process_categories(self, categories, parent=None):
        # Ищем категории, которые являются дочерними для данного родителя
        # children = [cat for cat in categories if (parent is None and '/' not in cat['path']) or (parent is not None and cat['path'].startswith(parent.path + '/'))]
        children = []
        for cat in categories:
            if parent is None and cat['path'].count('/') == 0:
                children.append(cat)
            elif parent is not None and cat['path'].startswith(parent.path + '/') and cat['path'].count('/') == parent.path.count('/') + 1:
                children.append(cat)

        for child in children:
            # Создаем новую категорию в базе данных
            print(child['name'])
            print(child['path'])
            print(child['url'])
            print('=== || ===')
            new_cat = Category.objects.create(
                name=child['name'],
                path=child['path'],
                url=child['url'],
                parent=parent,
            )

            # Рекурсивно обрабатываем дочерние категории
            self.process_categories(categories, parent=new_cat)

    def get_categories(self):
        url = "https://mpstats.io/api/wb/get/categories"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        print('get_categories', len(data))
        self.process_categories(data)
        return data
    
    def get_category(self, d1, d2, path, fbs):
        url = "https://mpstats.io/api/wb/get/category/items"
        params = {
            'd1': d1,
            'd2': d2,
            'path': path,
            'fbs': fbs
        }
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        return data
    
    def get_category_sellers(self, d1, d2, path, fbs):
        url = "https://mpstats.io/api/wb/get/category/sellers"
        params = {
            'd1': d1,
            'd2': d2,
            'path': path,
            'fbs': fbs
        }
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        return data


# mpstats = Mpstats()
# data = mpstats.get_category('2024-02-01', '2024-03-01', 'Женщинам', 1)
    
# curl --location --request GET 'https://mpstats.io/api/wb/get/category?d1=2024-02-01&d2=2024-03-01&path=Автотовары&fbs=1' \
# --header 'X-Mpstats-TOKEN: 65d78fba6d7824.982500042ed2ade776ce4f181ede657c3afab330' \
# --header 'Content-Type: application/json' \    


# 1 + 
# Стабильность среднего чека - изменение среднего чека 

# 2 -
# Монополия - объем продаж у топ 10 продавцов по обороту в 

# 3 +
# Оценка потенциала органических продаж - процент товаров 

# 4 +
# Среднее количество продаж у товаров

# 5 +
# Конкурентный ассортимент - количество товаров в нише
# items

# 6 +
# Оценка тренда продаж - сравнение среднесуточного оборота в начале и конца периода

# 7 +
# Объем рынка - оборот в нише в месяц. При изменении периода на 14 или 7 дней показатели делятся на 2 и 4 соответственно
    
# 8 +
# Востребованность ниши - изменение количества продавцов с начала периода
    
# 9 +
# Объем рынка (динамика)

# 10 +
# LP - Упущенная выручка в нише - для каждого товара считается как:  количество дней без продаж * среднее количество продаж товара в день. По нише считается как сумма упущенной выручки всех товаров в нише

# 11 -
# Объем рынка у топ 10 (динамика)
    
# 12 +
# SPP - Процент товаров с продажами (динамика)

# 13 +
# Средняя скорость продаж - среднее количество продаж в день по всем товарам, считается как: общее количество продаж ÷ общее количество товаров ÷ 30 (дней)

# 14 +
# Средний оборот на продавца

# 15 +
# SPS - процент продавцов с продажами