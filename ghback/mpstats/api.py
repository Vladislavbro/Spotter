import requests
from .models import Category, Subject
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Mpstats:
    headers = {
        'X-Mpstats-TOKEN': '661013e49bcf55.065063530218f7c2a8454fe95db3e56c776587c6',
        'Content-Type': 'application/json',
    }

    def __init__(self):
        pass

    def get_subjects(self, date=None):
        url = "https://mpstats.io/api/wb/get/subjects/select"
        if date:
            # YYYY-MM-DD
            url += f"?date={date}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data
    
    def get_yearly_data(self):
        data = []
        for i in range(12):
            date = (datetime.now() - relativedelta(months=i)).strftime('%Y-%m-01')
            subjects = self.get_subjects(date)
            data.extend(subjects)
        return data
    
    def get_trend(self, sales):
        sales = np.array(sales)
        months = np.array(range(1, len(sales) + 1))
        # Шаг 1: Рассчитаем тренд с использованием линейной регрессии
        A = np.vstack([months, np.ones(len(months))]).T
        trend_coeff, intercept = np.linalg.lstsq(A, sales, rcond=None)[0]
        trend = trend_coeff * months + intercept
        # Шаг 2: Рассчитаем коэффициент как отношение продаж к тренду
        coefficients = sales / trend
        # result = np.vstack([months, sales, trend, coefficients]).T
        return coefficients

    def process_yearly_data(self):
        data = self.get_yearly_data()
        df = pd.DataFrame(data)
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
        trends = {}
        for id in df['id'].unique():
            id_data = df[df['id'] == id]
            revenue = id_data['revenue']
            revenue.reverse()
            print('revenue', revenue)
            trend = self.get_trend(revenue)
            print('trend', trend)
            trends[id] = trend
        return trends
    
    def calculate_subjects(self):
        subjects = self.get_subjects()
        trends = self.process_yearly_data()
        for subject in subjects:
            try:
                subject_db = Subject.objects.get(mpstats_id=subject['id'])
            except Subject.DoesNotExist:
                subject_db = Subject(mpstats_id=subject['id'])
            scoring = 0
            # Выручка
            subject['calculate'] = {}
            if subject['revenue'] >= 80000000:
                scoring += 1
                subject['calculate']['revenue'] = 1
            elif subject['revenue'] <= 10000000:
                scoring -= 1
                subject['calculate']['revenue'] = -1
            # Медианная сумма продаж на одного продавца
            if subject['revenue'] / subject['suppliers'] >= 20000:
                scoring += 1
                subject['calculate']['revenue/suppliers'] = 1
            elif subject['revenue'] / subject['suppliers'] <= 10000:
                scoring -= 1
                subject['calculate']['revenue/suppliers'] = -1
            # Количество товаров
            if subject['items'] < 1000:
                scoring += 1
                subject['calculate']['items'] = 1
            elif subject['items'] > 2000:
                scoring -= 1
                subject['calculate']['items'] = -1
            # Выручка на товар
            if subject['revenue'] / subject['items'] >= 20000:
                scoring += 1
                subject['calculate']['revenue/items'] = 1
            elif subject['revenue'] / subject['items'] <= 10000:
                scoring -= 1
                subject['calculate']['revenue/items'] = -1
            # Оборачиваемость в днях
            if subject['turnover_days'] < 20:
                scoring += 1
                subject['calculate']['turnover_days'] = 1
            elif subject['turnover_days'] > 50:
                scoring -= 1
                subject['calculate']['turnover_days'] = -1
            # Количество продавцов
            if subject['suppliers'] < 1000:
                scoring -= 1
                subject['calculate']['suppliers'] = -1
            elif subject['suppliers'] < 5000:
                scoring += 1
                subject['calculate']['suppliers'] = 1
            # Количество продавцов с продажами
            if subject['suppliers_with_sells'] / subject['suppliers'] > 0.5:
                scoring += 1
                subject['calculate']['suppliers_with_sells/suppliers'] = 1
            elif subject['suppliers_with_sells'] / subject['suppliers'] < 0.2:
                scoring -= 1
                subject['calculate']['suppliers_with_sells/suppliers'] = -1
            # Средний процент выкупа с учетом возвратов
            if subject['purchase_after_return'] >= 90:
                scoring += 1
                subject['calculate']['purchase_after_return'] = 1
            elif subject['purchase_after_return'] < 40:
                scoring -= 1
                subject['calculate']['purchase_after_return'] = -1
            # Средняя цена по товарам с продажами
            if (subject['final_price_average_with_sells'] or 0) >= 1500:
                scoring += 1
                subject['calculate']['final_price_average_with_sells'] = 1
            elif (subject['final_price_average_with_sells'] or 0) < 750:
                scoring -= 1
                subject['calculate']['final_price_average_with_sells'] = -1
            # Сезонность (доп 12 запросов за прошлый календарный год)
            trend = trends[subject['id']]
            subject['calculate']['trend'] = list(trend)
            trend_coef = self.get_trend_coef(trend)
            subject['calculate']['trend_coef'] = trend_coef
            scoring += trend_coef

            subject_db.data = subject
            subject_db.scoring = scoring
            subject_db.save()

    def get_trend_coef(self, array):
        all_in_range_0_7_to_1_3 = True
        all_in_range_0_4_to_2_5 = True
        
        for number in array:
            if number < 0.4 or number > 2.5:
                return -1
            if number < 0.7 or number > 1.3:
                all_in_range_0_7_to_1_3 = False
            if number < 0.4 or number > 2.5:
                all_in_range_0_4_to_2_5 = False
        
        if all_in_range_0_7_to_1_3:
            return 1
        elif all_in_range_0_4_to_2_5:
            return 0
        else:
            return -1

    def get_subcategories(self, path):
        url = f"https://mpstats.io/api/wb/get/category/subcategories?path={path}"
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

# Выручка (revenue) +
# Упущенная выручка +
# Количество товаров (items) +
# Выручка на товар (revenue / items) +
# Количество продавцов (suppliers) +
# Количество продавцов с продажами +
# Средний процент выкупа с учетом возвратов (purchase_after_return среднее?)
# Средняя цена по товарам с продажами (final_price_average_with_sells) +
# Сезонность (sales / sales среднее)

# 1
# subjects select
# {"id":8640,"days":30,"items":19,"live_items":4,"items_with_sells":4,"live_items_percent":21.05,"items_with_sells_percent":21.05,"brands":9,"brands_with_sells":2,"brands_with_sells_percent":22.22,"suppliers":9,"suppliers_with_sells":2,"suppliers_with_sells_percent":22.22,"sales":11,"revenue":29165,"final_price_min":1803,"final_price_max":26524,"final_price_average":8835.58,"final_price_median":5904,"final_price_min_with_sells":1803,"final_price_max_with_sells":4920,"final_price_average_with_sells":3297.75,"final_price_median_with_sells":3234,"rating_average":4.83,"card_rating_average":44.21,"comment_valuation_average":4.6427,"rating_with_sells":5,"card_rating_with_sells":62.75,"comment_valuation_with_sells":4.7975,"count_total":1,"items_with_stocks":1,"turnover_days":3,"turnover_once":11,"new_items":7,"revenue_potential":76932,"lost_profit":47767,"lost_profit_percent":62.09,"open_card_count":0,"add_to_cart_percent":0,"cart_to_order_percent":0,"category":"Мототовары","name":"Мотокофры","commision_fbo":16.5,"commision_fbs":16.5,"basic_logistics":0,"cost_pallet":0,"storage_price":0,"acceptance_price":0,"delivery_by_volume":0,"purchase":0,"purchase_after_return":0,"orders_count":0,"warehouses":[]}
# 2
# curl --location --request GET 'https://mpstats.io/api/wb/get/subject/price_segmentation?path=8640' \
# --header 'X-Mpstats-TOKEN: 661013e49bcf55.065063530218f7c2a8454fe95db3e56c776587c6' \
# --header 'Content-Type: application/json'

# [
#     {
#         "range":"1803-3567",
#         "items":6,
#         "items_with_sells":3,
#         "brands":4,
#         "brands_with_sells":2,
#         "sellers":4,
#         "sellers_with_sells":2,
#         "revenue":24125,
#         "sales":10,
#         "product_revenue":8041,
#         "min_range_price":1803,
#         "max_range_price":3567,
#         "revenue_potential":323655,
#         "lost_profit":299530,
#         "lost_profit_percent":92
#     },
#     {"range":"3640-6314","items":6,"items_with_sells":1,"brands":4,"brands_with_sells":1,"sellers":4,"sellers_with_sells":1,"revenue":5040,"sales":1,"product_revenue":5040,"min_range_price":3640,"max_range_price":6314,"revenue_potential":151200,"lost_profit":146160,"lost_profit_percent":96},
#     {"range":"7062-24587","items":6,"items_with_sells":0,"brands":3,"brands_with_sells":0,"sellers":3,"sellers_with_sells":0,"revenue":0,"sales":0,"product_revenue":0,"min_range_price":7062,"max_range_price":24587,"revenue_potential":0,"lost_profit":0,"lost_profit_percent":0},
#     {"range":"24587-26524","items":1,"items_with_sells":0,"brands":1,"brands_with_sells":0,"sellers":1,"sellers_with_sells":0,"revenue":0,"sales":0,"product_revenue":0,"min_range_price":26524,"max_range_price":26524,"revenue_potential":0,"lost_profit":0,"lost_profit_percent":0}
# ]