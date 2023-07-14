from django.db.models import Sum, Avg, Q, Count
from api.models import Product, ProductStat, Config, Query
from datetime import datetime, timedelta


def calculate_query(query):
    update = {}
    product_ids = Product.objects.filter(
        root=query.root, features__contains=query.features
    ).values_list('id', flat=True)
    update['products_count'] = product_ids.count()
    if update['products_count'] == 0:
        return
    productstats_current = ProductStat.objects.filter(
        parsing_id=config.current_parsing_id,
        product_id__in=product_ids
    )
    print('productstats_current', productstats_current.explain())
    last_agg_values = productstats_current.values(
        'sales_7_fbo', 'sales_14_fbo', 'sales_30_fbo', 
        'sales_7_fbs', 'sales_14_fbs', 'sales_30_fbs')
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
    if productstats_current.count() < 11 or productstats_current.count() > 2500:
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
        print('productstats', period, productstats.explain())
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
        print('productstats_prev', period, productstats_prev.explain())
        agg_prev = productstats_prev.aggregate(
            Avg('price'),
            Sum('profit_fbo'),
            Sum('profit_fbs'),
        )
        for fb in ['fbo', 'fbs']:
            field = f'profit_{period}_{fb}'
            pstats = productstats_current.order_by(f'-{field}')[:10].values()
            print(fb, period, pstats.explain())
            if pstats.count() < 10:
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
            if update[f'price_avg_{period}'] < agg_prev['price__avg'] * 0.6:
                continue
            if update[f'price_avg_{period}'] > agg_prev['price__avg'] * 1.4:
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


config = Config.objects.first()
query = Query.objects.filter(parsing_id=config.current_parsing_id,).exclude(calculated=True).first()
calculate_query(query)