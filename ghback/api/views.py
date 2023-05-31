import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.forms.models import model_to_dict
from django.db.models import Avg, Sum, Count, Q
from api.models import Customer, Order, Config
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# from dateutil.relativedelta import relativedelta
import threading
import csv
# import requests
from api.parse import Parser
from api.migrate import Migrate
from api.models import (Category, Product, ProductStat, 
                        Config, Query, CategoryStat)
from api.parse import nlp


def me(request):
    print(' --- me --- ', request.get_host())
    if request.user.is_authenticated:
        user = User.objects.prefetch_related('customer').filter(
            pk=request.user.id).values(
                'id', 'username', 'email', 'first_name', 'last_name',
                'customer__subscribe_type', 'customer__subscribe_until',
                'is_staff', 'is_superuser').first()
        return JsonResponse(user)
    elif request.get_host() == 'test.spotter.fun':
        user = authenticate(username='Тест', password='123')
        login(request, user)
        return JsonResponse(
            User.objects.prefetch_related('customer').filter(
                email='test@test.ru'
            ).values(
                'id', 'username', 'email', 'first_name', 'last_name',
                'customer__subscribe_type', 'customer__subscribe_until',
                'is_staff', 'is_superuser'
            ).first()
        )
    else:
        response = JsonResponse({})
        response.set_cookie('csrftoken', get_token(request))
        return response


def log_in(request):
    body = json.loads(request.body)
    print('log_in', body)
    user = authenticate(username=body['username'].strip(),
                        password=body['password'])
    if user is not None:
        login(request, user)  # and request.user.__class__ is not AnonymousUser:
        print('body', body, user, request.user)
        user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
        return JsonResponse(user)
    else:
        return JsonResponse({'status': 'not auth'})


def log_out(request):
    logout(request)
    return HttpResponse('')


def signup(request):
    body = json.loads(request.body)
    if body['password'] != body['password_confirm']:
        return JsonResponse({
            'status': 'error',
            'message': 'Пароли не совпадают'})
    if User.objects.filter(email=body['email'].strip()).first():
        return JsonResponse({
            'status': 'error',
            'message': (
                'Пользователь с таким email уже существует, '
                'выберите другой или восстановите пароль.'
            )})
    user = User(
        username=body['username'].strip(),
        email=body['email'].strip(),
        last_name=body['last_name'].strip(),
        first_name=body['first_name'].strip(),
    )
    user.set_password(body['password'])
    user.save()
    customer = Customer(
        user=user
    )
    customer.save()
    login(request, user)
    return JsonResponse({'status': 'success', 'user': model_to_dict(user)})


def accounts(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user.is_superuser:
            accounts = User.objects.prefetch_related('customer').all().values(
                'id', 'username', 'email', 'first_name', 'last_name',
                'customer__subscribe_type', 'customer__subscribe_until',
                'is_staff', 'is_superuser')
            return JsonResponse({'accounts': list(accounts)})
    return JsonResponse({'accounts': []})


def account(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user.is_superuser:
            body = json.loads(request.body)
            if body.get('id'):
                user = User.objects.get(pk=body.get('id'))
                user.first_name = body.get('first_name')
                user.last_name = body.get('last_name')
                user.save()
                if body.get('subscribe_until'):
                    customer = Customer.objects.get(user=user)
                    customer.subscribe_until = body['subscribe_until']
                    customer.subscribe_type = body['subscribe_type']
                    customer.save()
                user = User.objects.prefetch_related('customer').filter(
                    pk=body.get('id')).values(
                        'id', 'username', 'email', 'first_name', 'last_name',
                        'customer__subscribe_type',
                        'customer__subscribe_until', 'is_staff',
                        'is_superuser').first()
                return JsonResponse(user)
            else:
                if User.objects.filter(email=body['email'].strip()).first():
                    return JsonResponse({
                        'status': 'error',
                        'message': (
                            'Пользователь с таким email уже существует, '
                            'выберите другой или восстановите пароль.'
                        )})
                if User.objects.filter(username=body['username'].strip()).first():
                    return JsonResponse({
                        'status': 'error',
                        'message': (
                            'Пользователь с таким логином уже существует, '
                            'выберите другой или восстановите пароль.'
                        )})
                user = User(
                    username=body['username'].strip(),
                    email=body['email'].strip(),
                    last_name=body['last_name'].strip(),
                    first_name=body['first_name'].strip(),
                )
                user.set_password(body['password'])
                user.save()
                customer = Customer(
                    user=user
                )
                customer.save()
                if body.get('subscribe_until'):
                    customer.subscribe_until = body['subscribe_until']
                    customer.subscribe_type = body['subscribe_type']
                    customer.save()
                return JsonResponse(User.objects.prefetch_related(
                    'customer').filter(pk=user.id).values(
                        'id', 'username', 'email', 'first_name', 'last_name',
                        'customer__subscribe_type',
                        'customer__subscribe_until', 'is_staff',
                        'is_superuser').first())
    return JsonResponse({})


def delete_account(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user.is_superuser:
            User.objects.get(pk=id).delete()
    return JsonResponse({})


@csrf_exempt
def payment(request):
    body = json.loads(request.body)
    print('payment', body)
    if body['Success'] and body['Status'] == 'CONFIRMED':
        order = Order.objects.get(pk=body['OrderId'])
        order.paid = True
        order.save()
        user = order.user
        customer = Customer.objects.get(user=user)
        customer.subscribe_type = order.subscribe_type
        customer.subscribe_until = int((datetime.now() + relativedelta(months=1)).timestamp())
        customer.save()
    # payment {'TerminalKey': '1664189383150', 'OrderId': '4', 'Success': True, 'Status': 'CONFIRMED', 'PaymentId': 2298207035, 'ErrorCode': '0', 'Amount': 1900, 'CardId': 276988801, 'Pan': '553420******8996', 'ExpDate': '0929', 'Token': '90892c775d31abd05ae5747a132dfdb78da6721509365f38eb483410db9ec6e4'}
    return HttpResponse('ok')


def order(request):
    body = json.loads(request.body)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.filter(
            user=user,
            paid=False
        ).first()
        if order is None:
            order = Order(
                user=user,
            )
        order.amount = body['amount']
        order.subscribe_type = body['subscribe_type']
        order.date = datetime.now()
        order.save()
        return JsonResponse({'order': {
            'id': order.id,
            'user': order.user_id,
            'paid': order.paid,
            'subscribe_type': order.subscribe_type,
            'date': order.date,
        }})
    else:
        return JsonResponse({})


def parser(request):
    native_ids = [t.native_id for t in threading.enumerate()]
    config = Config.objects.first()
    if config.thread_id not in native_ids:
        t = threading.Thread(target=Parser, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
        print('t.native_id', t.native_id)
        config.thread_id = t.native_id
        config.save()
        print('config', model_to_dict(config))
    return JsonResponse({
        'native_ids': native_ids,
        'active_count': threading.active_count(),
        'status': 'success'
    })


def get_children(category, categories, stats, period, fb):
    return [{
        **c,
        'items': get_children(c, categories, stats, period, fb),
        'stat': [{
            'products_count': s['products_count'],
            'products_solded': s[f'products_solded_{period}_{fb}'],
            'sellers_count': s[f'sellers_count_{period}'],
            'sellers_solded': s[f'sellers_solded_{period}_{fb}'],
            'profit': s[f'profit_{period}_{fb}'],
            'price_avg': s[f'price_avg_{period}'],
        } for s in stats if s['category_id'] == category['id']]
    } for c in categories if c.get('parent') == category['wb_id']]


def get_rows(rows, category, categories, stats, period, fb, parent=None):
    stat = [s for s in stats if s['category_id'] == category['id']]
    if parent:
        name = parent['name'] + ' > ' + category['name']
    else:
        name = category['name']
    if len(stat):
        # rows.append([name, None, None, None, None, None, None])
        # else:
        stat = stat[0]
        rows.append([
            name,
            stat['products_count'],
            stat[f'sellers_count_{period}'],
            stat[f'profit_{period}_{fb}'],
            stat[f'price_avg_{period}'],
            stat[f'sellers_solded_{period}_{fb}'],
            stat[f'products_solded_{period}_{fb}'],
        ])
    children = [c for c in categories if c.get('parent') == category['wb_id']]
    for child in children:
        get_rows(rows, child, categories, stats, period, fb, category)


def categories_list(request):
    output = request.GET.get('output', 'json')
    period = int(request.GET.get('period', '30'))
    fb = request.GET.get('fb', 'fbo')
    dateTo = request.GET.get('date')
    sort = request.GET.get('sort')
    config = None
    if dateTo:
        date = datetime.strptime(dateTo, '%Y-%m-%d').timestamp()
        config = Config.objects.filter(
            calculated=True,
            current_parsing_id__gte=date,
            # current_parsing_id__lt=date + 86400,
        ).first()
    out = []
    categories = Category.objects.all()
    sort = request.GET.get('sort')
    if sort is not None:
        direction = request.GET.get('direction')
        if direction == 'desc':
            direction = '-'
        else:
            direction = ''
        if sort == 'products_count':
            categories = categories.order_by(f'{direction}products_count')
        elif sort in ['price_avg', 'sellers_count']:
            categories = categories.order_by(f'{direction}{sort}_{period}')
        elif sort in ['products_solded', 'sellers_solded', 'profit']:
            categories = categories.order_by(f'{direction}{sort}_{period}_{fb}')
    categories = categories.values('id', 'name', 'parent', 'wb_id')
    category_ids = [c['id'] for c in categories]
    if config is None:
        # config = Config.objects.filter(calculated=True).first()
        stats = []
    else:
        stats = CategoryStat.objects.filter(
            category_id__in=category_ids,
            parsing_id=config.current_parsing_id).values()
    roots = [c for c in categories if c.get('parent') is None]
    if output == 'json':
        for root in roots:
            root['items'] = get_children(root, categories, stats, period, fb)
            # calc_stat(root)
            out.append(root)
        return JsonResponse({
            'total': categories.count(),
            'date': config.current_parsing_id if config else None,
            'items': out
        })
    elif output == 'csv':
        fields = ['Категория', 'Товары, шт.', 'Продавцов, шт.', 
                  'Оборот', 'Средняя цена', 'Продавцы с продажами',
                  'Товары с продажами']
        rows = []
        for root in roots:
            get_rows(rows, root, categories, stats, period, fb)
        filename = f'Категории_{dateTo}_{period}_{fb}.csv'
        file_path = f'export/{filename}'
        with open(file_path, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(rows)
        with open(file_path) as f:
            response = HttpResponse(f, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response


def queries_top(request):
    period = int(request.GET.get('period', '30'))
    output = request.GET.get('output', 'json')
    fb = request.GET.get('fb', 'fbo')
    page = int(request.GET.get('page', '1'))
    dateTo = request.GET.get('date')
    if dateTo:
        date = datetime.strptime(dateTo, '%Y-%m-%d').timestamp()
        config = Config.objects.filter(
            calculated=True,
            current_parsing_id__gte=date,
            current_parsing_id__lt=date + 86400,
        ).first()
        if config is None:
            return JsonResponse({
                'total': 0,
                'items': []
            })
    else:
        config = Config.objects.filter(calculated=True).first()
    items = Query.objects.filter(
        parsing_id=config.current_parsing_id,
        # products_count__lte=2500,
        # products_count__gte=10,
    )
    if request.GET.get('products_count'):
        start = request.GET['products_count'].split(';')[0]
        if start:
            items = items.filter(products_count__gte=int(start))
        end = request.GET['products_count'].split(';')[1]
        if end:
            items = items.filter(products_count__lte=int(end))
    if request.GET.get('price_avg'):
        start = request.GET['price_avg'].split(';')[0]
        if start:
            field = f'price_avg_{period}__gte'
            items = items.filter(**{field: start})
        end = request.GET['price_avg'].split(';')[1]
        if end:
            field = f'price_avg_{period}__lte'
            items = items.filter(**{field: end})
    if request.GET.get('profit'):
        start = request.GET['profit'].split(';')[0]
        if start:
            field = f'profit_{period}_{fb}__gte'
            items = items.filter(**{field: start})
        end = request.GET['profit'].split(';')[1]
        if end:
            field = f'profit_{period}_{fb}__lte'
            items = items.filter(**{field: end})
    for n in [1, 10]:
        if request.GET.get(f'product_{n}_profit'):
            start = request.GET[f'product_{n}_profit'].split(';')[0]
            if start:
                field = f'product_{n}_profit_{period}_{fb}__gte'
                items = items.filter(**{field: start})
            end = request.GET[f'product_{n}_profit'].split(';')[1]
            if end:
                field = f'product_{n}__profit_{period}_{fb}__lte'
                items = items.filter(**{field: end})
    # field = f'top_{period}_{fb}'
    # items = items.filter(**{ field: True})
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')
    if sort is not None:
        if direction == 'desc':
            direction = '-'
        else:
            direction = ''
        if sort == 'price_avg':
            sort += f'_{period}'
        if 'profit' in sort:
            sort += f'_{period}_{fb}'
        items = items.order_by(f'{direction}{sort}')
    if output == 'json':
        total = items.count()
        items = items[((page - 1) * 100):page * 100]
        return JsonResponse({
            'total': total,
            'items': [{
                'id': i['id'],
                'root': i['root'],
                'features': ' '.join(i['features']),
                'products_count': i['products_count'],
                'products_solded': i[f'products_solded_{period}_{fb}'],
                'product_1_profit': i[f'product_1_profit_{period}_{fb}'],
                'product_10_profit': i[f'product_10_profit_{period}_{fb}'],
                'price_avg': i[f'price_avg_{period}'],
                'profit': i[f'profit_{period}_{fb}'],
            } for i in items.values()]
        })
    elif output == 'csv':
        return export_queries(items, dateTo, period, fb)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Не задан формат вывода'
        })


def queries_search(request):
    view = request.GET.get('view')
    query = request.GET.get('query')
    doc = nlp(query)
    root = [w for w in doc if w.dep_ == 'ROOT'][0]
    if root.tag_ != 'NOUN':
        nsubj = [w for w in doc if w.dep_ == 'nsubj']
        if len(nsubj):
            root = nsubj[0]
    query_root = root.lemma_
    features = list(set([w.lemma_ for w in doc if w.tag_ == 'ADJ' and len(w.lemma_) > 1]))
    features.sort()
    query_features = features
    # query_root, query_features = 'рубашка', ['белый', 'офисный']
    period = int(request.GET.get('period', '30'))
    fb = request.GET.get('fb', 'fbo')
    dateTo = request.GET.get('date')
    if dateTo:
        date = datetime.strptime(dateTo, '%Y-%m-%d').timestamp()
        config = Config.objects.filter(
            calculated=True,
            current_parsing_id__gte=date,
            current_parsing_id__lt=date + 86400,
        ).first()
        if config is None:
            return JsonResponse({
                'status': 'error',
                'message': 'За выбранную дату нет данных'
            })
    else:
        config = Config.objects.filter(calculated=True).first()
    product_ids = Product.objects.filter(
        root=query_root,
        features__contains=query_features
    ).values_list('id', flat=True)
    total = product_ids.count()
    # if total > 1000:
    #     return JsonResponse({
    #         'status': 'error',
    #         'message': f'Найдено товаров {total}. Уточните запрос'
    #     })
    productstats = ProductStat.objects.prefetch_related('product').filter(
        parsing_id=config.current_parsing_id,
        product_id__in=product_ids
    )
    response = {}
    if 'products' in view:
        output = request.GET.get('output', 'json')
        page = int(request.GET.get('page', '1'))
        per_page = int(request.GET.get('per_page', '100'))
        sort = request.GET.get('sort')
        direction = request.GET.get('direction')
        if sort is not None:
            if direction == 'desc':
                direction = '-'
            else:
                direction = ''
            productstats = productstats.order_by(f'{direction}{sort}')
        if output == 'csv':
            fields = ['Наименование', 'Артикул', 'Рейтинг', 'Отзывов', 'Цена', 
                      'Цена без скидки', 'Продавец', 'Бренд', 'Оборот', 
                      'Продаж']
            rows = [list(row) for row in productstats.values_list(
                'product__name', 'product__articul', 'product__rating', 
                'product__feedbacks', 'price', 'priceU', 
                'product__supplier_id', 'product__brand_id', 
                f'profit_{period}_{fb}', f'sales_{period}_{fb}'
            )]
            filename = f'{query}_{dateTo}_{period}_{fb}.csv'
            file_path = f'export/{filename}'
            with open(file_path, 'w') as f:
                write = csv.writer(f)
                write.writerow(fields)
                write.writerows(rows)
            with open(file_path) as f:
                response = HttpResponse(f, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename={filename}'
                return response
        else:
            response['total'] = total
            response['items'] = list(productstats[((page - 1) * per_page):page * per_page].values(
                'id', 'price', 'priceU', f'profit_{period}_{fb}', 
                f'sales_{period}_{fb}', 'product__name', 'product__articul', 
                'product__name', 'product__rating', 'product__feedbacks',
            ))
    if 'graphs' in view:
        start = (datetime.now() - timedelta(days=30)).replace(
                hour=0, minute=0, second=0, microsecond=0).timestamp()
        end = datetime.now().timestamp()
        productstats = ProductStat.objects.prefetch_related('product').filter(
            parsing_id__gte=start,
            parsing_id__lt=end,
            product_id__in=product_ids
        )
        response['graphs'] = list(productstats.values('parsing_id').annotate(
            price=Avg('price'),
            profit=Sum(f'profit_{period}_{fb}'),
            sales=Sum(f'sales_{period}_{fb}'),
            products=Count('pk'),
            sellers=Count('product__supplier_id', distinct=True),
            brands=Count('product__brand_id', distinct=True)
        ))
    if 'summary' in view:
        sales_field = f'sales_30_{fb}__gt'
        sales_field_week = f'sales_14_{fb}__gt'
        curr_stat = productstats.aggregate(
            Avg('price'),
            Avg(f'sales_30_{fb}'),
            Sum(f'sales_30_{fb}'),
            Sum(f'profit_30_{fb}'),
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
        start = (datetime.now() - timedelta(days=30)).replace(
                hour=0, minute=0, second=0, microsecond=0)
        prev_parsing = Config.objects.filter(
            current_parsing_id__lt=start.timestamp()).first()
        prev_stat = ProductStat.objects.filter(
            product_id__in=product_ids,
            parsing_id=prev_parsing.current_parsing_id
        ).aggregate(Avg('price'))
        # f_p - first period
        f_p_date = (datetime.now() - timedelta(days=14)).replace(
            hour=0, minute=0, second=0, microsecond=0).timestamp()
        f_p_config = Config.objects.filter(
            calculated=True,
            current_parsing_id__gte=f_p_date,
        ).first()
        sales_field = f'sales_14_{fb}__gt'
        f_p_stat = ProductStat.objects.filter(
            product_id__in=product_ids,
            parsing_id=f_p_config.current_parsing_id
        ).aggregate(
            Sum(f'profit_14_{fb}'),
            product_solded=Count('pk', filter=Q(**{sales_field: 0})),
        )
        # 1 Стабильность среднего чека - изменение среднего чека 
        # в течение месяца
        if prev_stat['price__avg']:
            response['price_avg_diff'] = (curr_stat['price__avg'] / prev_stat['price__avg'])
        # 2 Монополия - объем продаж у топ 10 продавцов по обороту в 
        # данной нише относительного общего оборота по нише
        response['monopoly'] = (top_supplier_agg[f'profit_30_{fb}__sum'] / curr_stat[f'profit_30_{fb}__sum'])
        # 3 Оценка потенциала органических продаж - процент товаров 
        # с продажами от общего количества товаров
        response['sales_org'] = curr_stat['sales_org'] / total
        # 4 Среднее количество продаж у товаров
        response['sales_avg'] = curr_stat[f'sales_30_{fb}__avg']
        # 5 Конкурентный ассортимент - количество товаров в нише
        response['products_count'] = total
        # 6 Оценка тренда продаж - сравнение среднесуточного оборота
        # в начале и конца периода
        response['sales_trend'] = (curr_stat[f'profit_14_{fb}__sum'] / f_p_stat[f'profit_14_{fb}__sum'])
        # 7 Объем рынка - оборот в нише в месяц. При изменении периода 
        # на 14 или 7 дней показатели делятся на 2 и 4 соответственно
        response['profit'] = curr_stat[f'profit_30_{fb}__sum']
        # 8 Востребованность ниши - изменение количества продавцов 
        # с начала периода
        response['suppliers'] = curr_stat['product__supplier_id__count']
        # 9 Объем рынка (динамика)
        response['volume'] = (curr_stat[f'profit_14_{fb}__sum'] / f_p_stat[f'profit_14_{fb}__sum'])
        # 10 LP - Упущенная выручка в нише - для каждого товара считается 
        # как:  количество дней без продаж * среднее количество продаж 
        # товара в день. По нише считается как сумма упущенной выручки 
        # всех товаров в нише
        response['profit_lost'] = curr_stat[f'profit_lost_{fb}__sum']
        # 11 Объем рынка у топ 10 (динамика)
        response['profit_top_sup'] = top_supplier_agg[f'profit_30_{fb}__sum']
        # 12 SPP - Процент товаров с продажами (динамика)
        response['product_solded'] = (curr_stat['product_solded'] / f_p_stat['product_solded'])
        # 13 Средняя скорость продаж - среднее количество продаж в день по 
        # всем товарам, считается как: общее количество продаж ÷ общее 
        # количество товаров ÷ 30 (дней)
        response['sales_speed_avg'] = curr_stat[f'sales_30_{fb}__sum'] / total / 30
        # 14 Средний оборот на продавца
        response['supplier_profit_avg'] = (curr_stat[f'profit_30_{fb}__sum'] / curr_stat['product__supplier_id__count'])
        # 15 SPS - процент продавцов с продажами
        response['supplier_sold_count'] = curr_stat['sup_sold_count']
        # stat['score'] = 0
        # if stat['price_avg_diff'] is not None:
        #     if stat['price_avg_diff'] < 0.9:
        #         stat['score'] -= 1
        #     elif stat['price_avg_diff'] >= 0.9 and stat['price_avg_diff'] <= 1.1:
        #         stat['score'] += 1
    return JsonResponse(response)


def export_queries(items, dateTo, period, fb):
    fields = ['Наименование', 'Кол-во товаров', 'Товары с продажами', 
              'Оборот первого товара', 'Оборот десятого товара',
              'Средняя цена', 'Оборот']
    rows = [
        [i['name'], i['products_count'], i[f'products_solded_{period}_{fb}'],
         i[f'product_1_profit_{period}_{fb}'], 
         i[f'product_10_profit_{period}_{fb}'],
         i[f'price_avg_{period}'], i[f'profit_{period}_{fb}']] for i in items.values()
    ]
    filename = f'Топ_запросы_{dateTo}_{period}_{fb}.csv'
    file_path = f'export/{filename}'
    with open(file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    # f = open(file_path, 'r')
    # content = f.read()
    with open(file_path) as f:
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


def product(request, articul):
    period = int(request.GET.get('period', '30'))
    # fb = request.GET.get('fb', 'fbo')
    dateTo = request.GET.get('date')
    if dateTo:
        end = datetime.strptime(dateTo, '%Y-%m-%d').replace(
            hour=23, minute=59, second=59)
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
    else:
        end = datetime.now()
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
    product = Product.objects.filter(articul=articul).first()
    stats = product.productstat_set.filter(
        parsing_id__gte=start.timestamp(),
        parsing_id__lte=end.timestamp(),
    )
    if product:
        out = {
            'name': product.name,
            'articul': product.articul,
            'rating': product.rating,
            'feedbacks': product.feedbacks,
            'created_at': product.created_at.timestamp(),
            'price': product.price,
            'priceU': product.priceU,
            'categories': [],
            'supplier_id': product.supplier_id,
            'brand_id': product.brand_id,
            'brand': product.brand,
            'stats': [{
                'date': stat.parsing_id,
                'profit_fbo': stat.profit_fbo,
                'profit_fbs': stat.profit_fbs,
                'price': stat.price,
                'priceU': stat.priceU,
            } for stat in stats]
        }
        parent = Category.objects.filter(wb_id=product.categories[0]).first()
        while parent:
            out['categories'].insert(0, {
                'id': parent.wb_id,
                'name': parent.name,
            })
            parent = Category.objects.filter(wb_id=parent.parent).first()
        return JsonResponse(out)
    else:
        return JsonResponse({
            'status': 'error',
            'message': f'Товар с артикулом {articul} отсутствует в БД'
        })


@csrf_exempt
def transfer_config(request):
    body = json.loads(request.body)
    m = Migrate()
    pg_id = m.create_config(body)
    print('pg_id', pg_id)
    return HttpResponse(pg_id)


@csrf_exempt
def transfer_category(request):
    body = json.loads(request.body)
    m = Migrate()
    pg_id = m.create_category(body)
    print('pg_id', pg_id)
    return HttpResponse(pg_id)


@csrf_exempt
def transfer_query(request):
    body = json.loads(request.body)
    m = Migrate()
    pg_id = m.create_query(body)
    print('pg_id', pg_id)
    return HttpResponse(pg_id)


@csrf_exempt
def transfer_product(request):
    body = json.loads(request.body)
    m = Migrate()
    pg_id = m.create_product(body)
    print('pg_id', pg_id)
    return HttpResponse(pg_id)
