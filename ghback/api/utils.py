from api.models import Config, ProductStat, Customer
from django.db.models import Sum, Avg, Q, Count
from datetime import datetime, timedelta


def get_scoring_productstats(product_ids, config):
    # print('get_query_scoring', model_to_dict(query))

    date = datetime.now()
    fb = 'fbo'

    total = product_ids.count()
    productstats = ProductStat.objects.prefetch_related('product').filter(
        parsing_id=config.current_parsing_id,
        product_id__in=product_ids
    )
    f_p_date = (date - timedelta(days=14)).replace(
        hour=0, minute=0, second=0, microsecond=0).timestamp()
    f_p_config = Config.objects.filter(
        calculated=True,
        current_parsing_id__gte=f_p_date,
    ).exclude(pk=config.id).last()
    print('summary', f_p_date, f_p_config)
    if f_p_config is None:
        print('Нет данных по товарам')
        return
    sales_field = f'sales_30_{fb}__gt'
    sales_field_week = f'sales_14_{fb}__gt'
    curr_stat = productstats.aggregate(
        Avg('price'),
        Avg(f'sales_30_{fb}'),
        Sum(f'sales_30_{fb}'),
        Sum(f'profit_30_{fb}'),
        Sum(f'profit_{fb}'),
        Sum(f'profit_lost_{fb}'),
        Sum(f'profit_14_{fb}'),
        Count('product__supplier_id', distinct=True),
        sales_org=Count('pk', filter=Q(**{sales_field: 0})),
        product_solded=Count('pk', filter=Q(**{sales_field_week: 0})),
        sup_sold_count=Count('product__supplier_id', 
                             filter=Q(**{sales_field: 0}), distinct=True),
    )
    supplier_ids = list(productstats.exclude(
        product__supplier_id=None
    ).order_by(f'-profit_30_{fb}').values_list(
        'product__supplier_id', flat=True)[:50])
    top_supplier_ids = list(set(supplier_ids))[:10]
    top_supplier_agg = productstats.filter(
        product__supplier_id__in=top_supplier_ids
    ).aggregate(Sum(f'profit_30_{fb}'))
    #
    start = (date - timedelta(days=30)).replace(
            hour=0, minute=0, second=0, microsecond=0)
    prev_parsing = Config.objects.filter(
        current_parsing_id__gt=start.timestamp()
    ).exclude(pk__in=[config.id, f_p_config.id]).last()
    prev_stat = ProductStat.objects.filter(
        product_id__in=product_ids,
        parsing_id=prev_parsing.current_parsing_id
    ).aggregate(Avg('price'))
    
    sales_field = f'sales_14_{fb}__gt'
    f_p_stat = ProductStat.objects.prefetch_related('product').filter(
        product_id__in=product_ids,
        parsing_id=f_p_config.current_parsing_id
    )
    f_p_stat_agg = f_p_stat.aggregate(
        Sum(f'profit_14_{fb}'),
        Count('product__supplier_id', distinct=True),
        product_solded=Count('pk', filter=Q(**{sales_field: 0})),
    )
    f_p_supplier_ids = list(f_p_stat.exclude(
        product__supplier_id=None
    ).order_by(f'-profit_30_{fb}').values_list(
        'product__supplier_id', flat=True)[:50])
    f_p_top_supplier_ids = list(set(f_p_supplier_ids))[:10]
    f_p_top_supplier_agg = productstats.filter(
        product__supplier_id__in=f_p_top_supplier_ids
    ).aggregate(Sum(f'profit_30_{fb}'))
    response = {}
    # 1 Стабильность среднего чека - изменение среднего чека 
    # в течение месяца
    response['scoring'] = 0
    if prev_stat['price__avg']:
        response['price_avg_diff'] = (curr_stat['price__avg'] / prev_stat['price__avg'])
        if response['price_avg_diff'] <= 0.9:
            response['scoring'] -= 1
        elif response['price_avg_diff'] <= 1.1:
            response['scoring'] += 1
    # 2 Монополия - объем продаж у топ 10 продавцов по обороту в 
    # данной нише относительного общего оборота по нише
    if curr_stat[f'profit_30_{fb}__sum'] == 0:
        response['monopoly'] = 0
    else:
        response['monopoly'] = (top_supplier_agg[f'profit_30_{fb}__sum'] / curr_stat[f'profit_30_{fb}__sum'])
    if response['monopoly'] <= 0.25:
        response['scoring'] += 1
    elif response['monopoly'] > 0.5:
        response['scoring'] -= 1
    # 3 Оценка потенциала органических продаж - процент товаров 
    # с продажами от общего количества товаров
    response['sales_org'] = curr_stat['sales_org'] / total
    if response['sales_org'] > 0.5:
        response['scoring'] += 1
    elif response['sales_org'] < 0.3:
        response['scoring'] -= 1
    # 4 Среднее количество продаж у товаров
    response['sales_avg'] = curr_stat[f'sales_30_{fb}__avg']
    if response['sales_avg'] >= 12:
        response['scoring'] += 1
    # 5 Конкурентный ассортимент - количество товаров в нише
    response['products_count'] = total
    if response['products_count'] < 1000:
        response['scoring'] += 1
    elif response['products_count'] > 2000:
        response['scoring'] -= 1
    # 6 Оценка тренда продаж - сравнение среднесуточного оборота
    # в начале и конца периода
    response['sales_trend'] = (curr_stat[f'profit_14_{fb}__sum'] / f_p_stat_agg[f'profit_14_{fb}__sum'])
    if response['sales_trend'] <= 0.9:
        response['scoring'] -= 1
    elif response['sales_trend'] > 1.1:
        response['scoring'] += 1
    # 7 Объем рынка - оборот в нише в месяц. При изменении периода 
    # на 14 или 7 дней показатели делятся на 2 и 4 соответственно
    response['profit'] = curr_stat[f'profit_30_{fb}__sum']
    if response['profit'] < 1000000:
        response['scoring'] -= 1
    elif response['profit'] >= 5000000 and response['profit'] <= 100000000:
        response['scoring'] += 1
    elif response['profit'] > 100000000:
        response['scoring'] -= 1
    # 8 Востребованность ниши - изменение количества продавцов 
    # с начала периода
    response['suppliers'] = curr_stat['product__supplier_id__count']
    response['suppliers_diff'] = curr_stat['product__supplier_id__count'] / f_p_stat_agg['product__supplier_id__count']
    if response['suppliers_diff'] < 0.9:
        response['scoring'] -= 1
    if response['suppliers_diff'] <= 1.1:
        response['scoring'] += 1
    # 9 Объем рынка (динамика)
    response['volume'] = (curr_stat[f'profit_14_{fb}__sum'] / f_p_stat_agg[f'profit_14_{fb}__sum'])
    if response['volume'] >= 1.1:
        response['scoring'] += 1
    if response['volume'] <= 0.9:
        response['scoring'] -= 1
    # 10 LP - Упущенная выручка в нише - для каждого товара считается 
    # как:  количество дней без продаж * среднее количество продаж 
    # товара в день. По нише считается как сумма упущенной выручки 
    # всех товаров в нише
    response['profit_lost'] = curr_stat[f'profit_lost_{fb}__sum'] / curr_stat[f'profit_{fb}__sum']
    if response['profit_lost'] > 0.2:
        response['scoring'] += 1
    elif response['profit_lost'] <= 0.1:
        response['scoring'] -= 1
    # 11 Объем рынка у топ 10 (динамика)
    response['profit_top_sup'] = top_supplier_agg[f'profit_30_{fb}__sum']
    response['profit_top_sup_diff'] = top_supplier_agg[f'profit_30_{fb}__sum'] / f_p_top_supplier_agg[f'profit_30_{fb}__sum']
    if response['profit_top_sup_diff'] >= 1.1:
        response['scoring'] -= 1
    # 12 SPP - Процент товаров с продажами (динамика)
    response['product_solded_diff'] = (curr_stat['product_solded'] / f_p_stat_agg['product_solded'])
    if response['product_solded_diff'] >= 1.1:
        response['scoring'] += 1
    elif response['product_solded_diff'] <= 0.9:
        response['scoring'] -= 1
    # 13 Средняя скорость продаж - среднее количество продаж в день по 
    # всем товарам, считается как: общее количество продаж ÷ общее 
    # количество товаров ÷ 30 (дней)
    response['sales_speed_avg'] = curr_stat[f'sales_30_{fb}__sum'] / total / 30
    if response['sales_speed_avg'] >= 1:
        response['scoring'] += 1
    elif response['sales_speed_avg'] >= 0 and response['sales_speed_avg'] <= 0.3:
        response['scoring'] -= 1
    # 14 Средний оборот на продавца
    response['supplier_profit_avg'] = (curr_stat[f'profit_30_{fb}__sum'] / curr_stat['product__supplier_id__count'])
    if response['supplier_profit_avg'] >= 100000:
        response['scoring'] += 1
    elif response['supplier_profit_avg'] <= 20000:
        response['scoring'] -= 1
    # 15 SPS - процент продавцов с продажами
    response['supplier_sold_count'] = curr_stat['sup_sold_count']
    response['supplier_sold_diff'] = curr_stat['sup_sold_count'] / curr_stat['product__supplier_id__count']
    if response['supplier_sold_diff'] >= 0.5:
        response['scoring'] += 1
    elif response['supplier_sold_diff'] <= 0.2:
        response['scoring'] -= 1
    return response

 
def save_profile(backend, user, response, *args, **kwargs):
    print('backend, user, response', backend, user, response)
    if backend.name == 'vk-oauth2':
        user.email = response.get('email')
        user.username = response.get('screen_name') + ':' + str(response.get('id'))
        user.save()
        customer = Customer.objects.filter(user=user).first()
        if customer is None:
            customer = Customer.objects.create(user=user)
        customer.phone = response.get('phone')
        customer.save()