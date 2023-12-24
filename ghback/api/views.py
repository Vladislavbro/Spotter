import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.db.models import Avg, Sum, Count, Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# from dateutil.relativedelta import relativedelta
import threading
import csv
import re
import requests
from api.parse import Parser
from api.basket import Basket
from api.migrate import Migrate
from api.models import (Category, Product, ProductStat, 
                        Customer, Order, Config,
                        Config, Query, CategoryStat, Supplier)
from api.parse import nlp
from dotenv import load_dotenv
import os
import random
import string
import pymorphy2
from api.utils import get_scoring_productstats


morph = pymorphy2.MorphAnalyzer()
load_dotenv()
UNISENDER_KEY = os.getenv('UNISENDER_KEY')


def send_mail(subject, content, email, list_id):
    url = (
        f'https://api.unisender.com/ru/api/sendEmail?format=json&'
        f'api_key={UNISENDER_KEY}&email={email}&'
        'sender_name=SPOTTER.FUN&sender_email=hello@spotter.fun&'
        f'subject={subject}&body={content}&list_id={list_id}&lang=ru'
    )
    response = requests.get(url)
    data = response.json()
    print(data)


def send_mail_v2(subject, content, email, user_id):
    base_url = 'https://go1.unisender.ru/ru/transactional/api/v1'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-API-KEY': '66jjjtqjwg7d8eqmiouqcawca6n41qzr33w7hyfo'
    }
    request_body = {
        "message": {
            "recipients": [
            {
                "email": email,
                "substitutions": {
                    "CustomerId": user_id,
                    "to_name": "hello spotter"
                },
            }
            ],
            "tags": [
                "string1"
            ],
            "skip_unsubscribe": 0,
            "global_language": "ru",
            "template_engine": "simple",
            "global_substitutions": {
            "property1": "string",
            "property2": "string"
            },
            "global_metadata": {
                "property1": "string",
                "property2": "string"
            },
            "body": {
                "html": f"<p>{content}</p>",
                "plaintext": content,
                "amp": "<!doctype html><html amp4email><head> <meta charset=\"utf-8\"><script async src=\"https://cdn.ampproject.org/v0.js\"></script> <style amp4email-boilerplate>body{visibility:hidden}</style></head><body><p>{content}</p></body></html>"
            },
            "subject": subject,
            "from_email": "hello@spotter.fun",
            "from_name": "Spotter.fun",
            # "reply_to": "user@example.com",
            "track_links": 0,
            "track_read": 0,
            "bypass_global": 0,
            "bypass_unavailable": 0,
            "bypass_unsubscribed": 0,
            "bypass_complained": 0,
            "headers": {
                "X-MyHeader": "some data",
                "List-Unsubscribe": "<mailto: unsubscribe@example.com?subject=unsubscribe>, <http://www.example.com/unsubscribe/{{CustomerId}}>"
            }
        }
    }
    r = requests.post(base_url+'/email/send.json', json=request_body, headers=headers)
    r.raise_for_status()  # throw an exception in case of error
    print(r.json())


def me(request):
    if request.user.is_authenticated:
        user = User.objects.prefetch_related('customer').filter(
            pk=request.user.id).values(
                'id', 'email', 'first_name', 'last_name', 'customer__phone',
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
                'id', 'email', 'first_name', 'last_name', 'customer__phone',
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
    user = authenticate(username=body['email'].strip(),
                        password=body['password'])
    if user is not None:
        login(request, user)
        user = User.objects.filter(pk=request.user.id).values().first()
        return JsonResponse(user)
    else:
        return JsonResponse({'status': 'not auth'})


def change_password(request):
    body = json.loads(request.body)
    user = User.objects.get(pk=request.user.id)
    if user.check_password(body['password']):
        user.set_password(body['new_password'])
        user.save()
        send_mail_v2(
            subject='Пароль успешно изменен', 
            content='Email: ' + user.email + '<br>Пароль: ' + body['new_password'], 
            email=user.email, user_id=user.id)
        return JsonResponse({'status': 'success', 
                             'message': 'Пароль успешно изменен'})
    else:
        return JsonResponse({'status': 'error', 
                             'message': 'Пароль не подходит'})


def change_password_v2(request):
    email = request.GET.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        password = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=6))
        user.set_password(password)
        user.save()
        send_mail_v2(
            subject='Пароль успешно изменен', 
            content='Email: ' + user.email + '<br>Пароль: ' + password,
            email=user.email, user_id=user.id)
        return JsonResponse({'status': 'success',
                             'message': 'Новый пароль отправлен на email'})
    else:
        return JsonResponse({'status': 'error',
                             'message': 'Пользователь не найден'})


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
        username=body['email'].strip(),
        email=body['email'].strip(),
        last_name=body['last_name'].strip(),
        first_name=body['first_name'].strip(),
    )
    user.set_password(body['password'])
    user.save()
    customer = Customer(
        user=user,
        phone=body.get('phone', '').strip(),
        subscribe_type='demo',
        subscribe_until=(datetime.now() + timedelta(days=5)).timestamp()
    )
    customer.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    send_mail_v2(
        subject='Успешная регистрация на сайте SPOTTER.FUN!', 
        content='Email: ' + body['email'] + '<br>Пароль: ' + body['password'], 
        email=user.email, user_id=user.id)
    return JsonResponse({'status': 'success', 'user': model_to_dict(user)})


def accounts(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user.is_superuser:
            accounts = User.objects.prefetch_related('customer').all().values(
                'id', 'email', 'first_name', 'last_name', 'customer__phone',
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
                if body.get('phone'):
                    customer = Customer.objects.get(user=user)
                    customer.phone = body['phone']
                    customer.save()
                user = User.objects.prefetch_related('customer').filter(
                    pk=body.get('id')).values(
                        'id', 'email', 'first_name', 'last_name',
                        'customer__subscribe_type', 'customer__phone',
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
                user = User(
                    username=body['email'].strip(),
                    email=body['email'].strip(),
                    last_name=body['last_name'].strip(),
                    first_name=body['first_name'].strip(),
                )
                user.set_password(body['password'])
                user.save()
                customer = Customer(
                    user=user
                )
                if body.get('phone'):
                    customer.phone = body['phone']
                if body.get('subscribe_until'):
                    customer.subscribe_until = body['subscribe_until']
                    customer.subscribe_type = body['subscribe_type']
                customer.save()
                return JsonResponse(User.objects.prefetch_related(
                    'customer').filter(pk=user.id).values(
                        'id', 'email', 'first_name', 'last_name',
                        'customer__subscribe_type', 'customer__phone',
                        'customer__subscribe_until', 'is_staff',
                        'is_superuser').first())
    return JsonResponse({})


def delete_account(request, id):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        if current_user.is_superuser:
            User.objects.get(pk=id).delete()
    return JsonResponse({})


def orders_list(request, id):
    user = User.objects.get(pk=id)
    return JsonResponse({
        'orders': [{
            'id': order.id,
            'subscribe_type': order.subscribe_type,
            'amount': order.amount,
            'paid': order.paid,
            'date': order.date.timestamp(),
        } for order in user.order_set.all()]
    })


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


def baskets(request):
    native_ids = [t.native_id for t in threading.enumerate()]
    config = Config.objects.first()
    native_id = None
    if config.baskets_thread_id not in native_ids:
        t = threading.Thread(target=Basket, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
        native_id = t.native_id
        config.baskets_thread_id = t.native_id
        config.save()
        print('baskets', t.native_id)
    return JsonResponse({
        'native_id': native_id,
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
            'top': s[f'top_{period}_{fb}'],
        } for s in stats if s['category_id'] == c['id']]
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
            current_parsing_id__lte=date,
            # current_parsing_id__lt=date + 86400,
        ).first()
    else:
        config = Config.objects.filter(
            calculated=True,
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
    items = Query.objects.prefetch_related('first_product').filter(
        parsing_id=config.current_parsing_id,
        scoring__scoring__gt=0,
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
    if request.GET.get('products_solded'):
        start = request.GET['products_solded'].split(';')[0]
        if start:
            field = f'products_solded_{period}_{fb}__gte'
            items = items.filter(**{field: start})
        end = request.GET['products_solded'].split(';')[1]
        if end:
            field = f'products_solded_{period}_{fb}__lte'
            items = items.filter(**{field: end})
    if request.GET.get('scoring'):
        start = request.GET['scoring'].split(';')[0]
        if start:
            items = items.filter(scoring__scoring__gte=int(start))
        end = request.GET['scoring'].split(';')[1]
        if end:
            items = items.filter(scoring__scoring__lte=int(end))
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
        if sort == 'scoring':
            sort = 'scoring__scoring'
        items = items.order_by(f'{direction}{sort}')
    if output == 'json':
        total = items.count()
        items = items[((page - 1) * 100):page * 100]
        return JsonResponse({
            'total': total,
            'items': [{
                'id': i['id'],
                'product_id': i['first_product__id'],
                'product_name': get_product_name(i),
                'product_image': get_product_image(i),
                'product_articul': i['first_product__articul'],
                'scoring': i['scoring'],
                'root': i['root'],
                'features': ' '.join(i['features']),
                'products_count': i['products_count'],
                'products_solded': i[f'products_solded_{period}_{fb}'],
                'product_1_profit': i[f'product_1_profit_{period}_{fb}'],
                'product_10_profit': i[f'product_10_profit_{period}_{fb}'],
                'price_avg': i[f'price_avg_{period}'],
                'profit': i[f'profit_{period}_{fb}'],
            } for i in items.values(
                'first_product__id', 'first_product__name', 'first_product__articul', 
                'first_product__basket',
                'id', 'scoring', 'root', 'features', 
                'products_count', f'products_solded_{period}_{fb}', 
                f'product_1_profit_{period}_{fb}', f'product_10_profit_{period}_{fb}',
                f'price_avg_{period}', f'profit_{period}_{fb}'
            )]
        })
    elif output == 'csv':
        return export_queries(items, dateTo, period, fb)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Не задан формат вывода'
        })


def get_product_image(product):
    basket = product['first_product__basket']
    articul = product['first_product__articul']
    if basket is None:
        return None
    image_url = f'https://basket-{basket}.wb.ru/'
    image_url += f'vol{str(articul)[:4]}/part{str(articul)[:6]}/'
    image_url += f'{articul}/images/big/1.webp'
    return image_url


def get_product_name(query):
    name = query['first_product__name']
    name = re.sub('[^a-zA-Zа-яА-Я0-9]', ' ', name)
    name = re.sub('\s+', ' ', name).strip()
    if name is None:
        words = [query['root']] + query['features'][:2]
        return ' '.join(words)
    words = name.split(' ')
    if len(words) > 3 and morph.parse(words[2])[0].tag.POS == 'PREP':
        return ' '.join(name.split(' ')[:4])
    return ' '.join(name.split(' ')[:3])


def get_keys(query):
    query = re.sub(r'[\W\d]', ' ', query)
    query = re.sub(r'\s+', ' ', query)
    doc = nlp(query.strip())
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
    return root[0].lemma_ if len(root) else None, [f.lemma_ for f in features]


def queries_search(request):
    view = request.GET.get('view')
    query = request.GET.get('query')
    if request.GET.get('product_id'):
        product_id = int(request.GET.get('product_id'))
        product = Product.objects.get(pk=product_id)
        query_root, query_features = product.root, product.features
    else:
        product_id = None
        query_root, query_features = get_keys(query)
    # query_root, query_features = 'рубашка', ['белый', 'офисный']
    period = int(request.GET.get('period', '30'))
    fb = request.GET.get('fb', 'fbo')
    dateTo = request.GET.get('date')
    date = datetime.now()
    if dateTo:
        date = datetime.strptime(dateTo, '%Y-%m-%d')
        config = Config.objects.filter(
            queries_calculated=True,
            current_parsing_id__gte=date.timestamp(),
        ).first()
        print('config', config.id, date)
        if config is None:
            return JsonResponse({
                'status': 'error',
                'message': 'За выбранную дату нет данных'
            })
    else:
        config = Config.objects.filter(queries_calculated=True).first()
        print('config', config.id, date)
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
    ps_count = productstats.count()
    print(total, ps_count)
    if ps_count == 0:
        return JsonResponse({
            'status': 'error',
            'message': f'Нет данных по товарам'
        })
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
                'product__rating', 'product__feedbacks', 'product__supplier_id',
                'product__brand', 'product__brand_id', 'product__articul'
            ))
            supplier_ids = [p['product__supplier_id'] for p in response['items']]
            suppliers = Supplier.objects.filter(wb_id__in=supplier_ids).values()
            for item in response['items']:
                supplier = [s for s in suppliers if s['wb_id'] == item['product__supplier_id']]
                if len(supplier):
                    item['supplier'] = supplier[0]
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
            profit=Sum(f'profit_{fb}'),
            sales=Sum(f'sales_{fb}'),
            products=Count('pk'),
            sellers=Count('product__supplier_id', distinct=True),
            brands=Count('product__brand_id', distinct=True)
        ))
    if 'summary' in view:
        if product_id:
            query = Query.objects.filter(
                parsing_id=config.current_parsing_id,
                first_product=product_id
            ).first()
            if query:
                scoring = query.scoring
            else:
                scoring = get_scoring_productstats(product_ids, config)
        else:
            scoring = get_scoring_productstats(product_ids, config)
        response.update(scoring)
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
        supplier = Supplier.objects.filter(wb_id=product.supplier_id).first()
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
            'supplier': model_to_dict(supplier) if supplier else None,
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


def brand(request, brandId):
    view = request.GET.get('view', '')
    period = int(request.GET.get('period', '30'))
    dateTo = request.GET.get('date')
    if dateTo:
        end = datetime.strptime(dateTo, '%Y-%m-%d').replace(
            hour=23, minute=59, second=59)
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
        config = Config.objects.filter(
            calculated=True,
            current_parsing_id__lte=end.timestamp(),
        ).first()
    else:
        end = datetime.now()
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
        config = Config.objects.filter(calculated=True).first()
    product_ids = Product.objects.filter(
        brand_id=brandId,
    ).values_list('id', flat=True)
    total = product_ids.count()
    response = dict()
    if 'graphs' in view:
        productstats = ProductStat.objects.prefetch_related('product').filter(
            parsing_id__gte=start.timestamp(),
            parsing_id__lte=end.timestamp(),
            product_id__in=product_ids
        )
        response['graphs'] = list(productstats.values('parsing_id').annotate(
            price=Avg('price'),
            profit_fbo=Sum('profit_fbo'),
            profit_fbs=Sum('profit_fbs'),
            sales_fbo=Sum('sales_fbo'),
            sales_fbs=Sum('sales_fbs'),
        ))
    if 'suppliers' in view:
        supplier_ids = list(Product.objects.filter(
            brand_id=brandId,
        ).values_list('supplier_id', flat=True))
        response['suppliers'] = list(
            Supplier.objects.filter(wb_id__in=supplier_ids).values()
        )
    if 'products' in view:
        page = int(request.GET.get('page', '1'))
        per_page = int(request.GET.get('per_page', '100'))
        sort = request.GET.get('sort')
        direction = request.GET.get('direction')
        fb = 'fbo'
        productstats = ProductStat.objects.prefetch_related('product').filter(
            parsing_id=config.current_parsing_id,
            product_id__in=product_ids
        )
        if sort is not None:
            if direction == 'desc':
                direction = '-'
            else:
                direction = ''
            productstats = productstats.order_by(f'{direction}{sort}')
        response['total'] = total
        response['items'] = list(productstats[((page - 1) * per_page):page * per_page].values(
            'id', 'price', 'priceU', f'profit_{period}_{fb}', 
            f'sales_{period}_{fb}', 'product__name', 'product__articul', 
            'product__rating', 'product__feedbacks', 'product__supplier_id',
            'product__brand', 'product__brand_id'
        ))
        supplier_ids = [p['product__supplier_id'] for p in response['items']]
        suppliers = Supplier.objects.filter(wb_id__in=supplier_ids).values()
        for item in response['items']:
            supplier = [s for s in suppliers if s['wb_id'] == item['product__supplier_id']]
            if len(supplier):
                item['supplier'] = supplier[0]
    return JsonResponse(response)


def supplier(request, supplierId):
    view = request.GET.get('view')
    period = int(request.GET.get('period', '30'))
    dateTo = request.GET.get('date')
    if dateTo:
        end = datetime.strptime(dateTo, '%Y-%m-%d').replace(
            hour=23, minute=59, second=59)
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
        config = Config.objects.filter(
            calculated=True,
            current_parsing_id__lte=end.timestamp(),
        ).first()
    else:
        end = datetime.now()
        start = (end - timedelta(days=period)).replace(
            hour=0, minute=0, second=0)
        config = Config.objects.filter(calculated=True).first()
    product_ids = Product.objects.filter(
        supplier_id=supplierId,
    ).values_list('id', flat=True)
    total = product_ids.count()
    response = dict()
    if 'graphs' in view:
        productstats = ProductStat.objects.prefetch_related('product').filter(
            parsing_id__gte=start.timestamp(),
            parsing_id__lte=end.timestamp(),
            product_id__in=product_ids
        )
        response['graphs'] = list(productstats.values('parsing_id').annotate(
            price=Avg('price'),
            profit_fbo=Sum('profit_fbo'),
            profit_fbs=Sum('profit_fbs'),
            sales_fbo=Sum('sales_fbo'),
            sales_fbs=Sum('sales_fbs'),
        ))
    if 'brands' in view:
        response['brands'] = list(Product.objects.filter(
            supplier_id=supplierId,
        ).values('brand', 'brand_id').distinct())
    if 'products' in view:
        page = int(request.GET.get('page', '1'))
        per_page = int(request.GET.get('per_page', '100'))
        sort = request.GET.get('sort')
        direction = request.GET.get('direction')
        fb = 'fbo'
        productstats = ProductStat.objects.prefetch_related('product').filter(
            parsing_id=config.current_parsing_id,
            product_id__in=product_ids
        )
        if sort is not None:
            if direction == 'desc':
                direction = '-'
            else:
                direction = ''
            productstats = productstats.order_by(f'{direction}{sort}')
        response['total'] = total
        response['items'] = list(productstats[((page - 1) * per_page):page * per_page].values(
            'id', 'price', 'priceU', f'profit_{period}_{fb}', 
            f'sales_{period}_{fb}', 'product__name', 'product__articul', 
            'product__rating', 'product__feedbacks', 'product__supplier_id',
            'product__brand', 'product__brand_id'
        ))
        supplier_ids = [p['product__supplier_id'] for p in response['items']]
        suppliers = Supplier.objects.filter(wb_id__in=supplier_ids).values()
        for item in response['items']:
            supplier = [s for s in suppliers if s['wb_id'] == item['product__supplier_id']]
            if len(supplier):
                item['supplier'] = supplier[0]
    return JsonResponse(response)


def search(request):
    query = request.GET.get('query')
    views = ['products', 'categories', 'brands', 'suppliers', 'keys']
    view = request.GET.get('view')
    response = {
        'query': query,
        'view': view,
    }
    if view not in views:
        message = (
            'Необходимо выбрать что искать, '
            f'варианты: {", ".join(views)}'
        )
        response['message'] = message

    if view == 'products':
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(articul__icontains=query)
        )
        response['items'] = list(products.values(
            'id', 'name', 'articul', 'basket', 'brand', 'brand_id',
            'supplier_id', 'rating', 'feedbacks', 'price',
            'priceU'
        )[:50])

    if view == 'categories':
        categories = Category.objects.filter(name__icontains=query)
        response['items'] = list(categories.values()[:50])

    if view == 'brands':
        products = Product.objects.filter(brand__icontains=query)
        brands = list(products.values('brand', 'brand_id').distinct()[:50])
        response['items'] = brands

    if view == 'suppliers':
        suppliers = Supplier.objects.filter(
            Q(name__icontains=query) | 
            Q(trademark__icontains=query)
        )
        response['items'] = list(suppliers.values()[:50])

    if view == 'keys':
        root, features = get_keys(query)
        names = list(Product.objects.filter(
            root=root, features__contains=features
        ).values('name').distinct()[:100])
        # words = [n['name'].lower().split(' ') for n in names]
        variants = []
        for name in names:
            name = re.sub(r'\W', ' ', name['name'])
            name = re.sub(r'\s+', ' ', name)
            words = name.lower().split(' ')
            if root in words:
                variant = []
                index = words.index(root)
                variant.append(words[index])
                if len(words) > index + 1:
                    if len(words[index + 1]) > 2:
                        variant.append(words[index + 1])
                    elif len(words) > index + 2 and len(words[index + 2]) > 2:
                        variant += words[index + 1:index + 3]
                if len(variant) > 1:
                    variants.append(' '.join(variant))
        response['features'] = features
        response['root'] = root
        response['variants'] = list(set(variants))

    return JsonResponse(response)


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
