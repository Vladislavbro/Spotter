import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.forms.models import model_to_dict
from api.models import Customer, Order, Config
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# from dateutil.relativedelta import relativedelta
import threading
import csv
# import requests
from api.parse import Parser
from api.migrate import Migrate
from api.mongo_models import Categories, Products, Queries
from api.mongo_models import Config as ConfigMongo
from api.models import Category, Product, Config, Query


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


def get_children(category, categories):
    return [{
        **c,
        'children': get_children(c, categories)
    } for c in categories if c.get('parent') == category['wb_id']]


def categories_list(request):
    out = []
    categories = Category.objects.all().values()
    for root in [c for c in categories if c.get('parent') is None]:
        root['children'] = get_children(root, categories)
        out.append(root)
    return JsonResponse({
        'categories': out
    })


def queries_top(request):
    period = int(request.GET.get('period', '30'))
    fb = request.GET.get('fb', 'fbo')
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')
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
        products_count__lte=2500,
        products_count__gte=10,
    )
    # field = f'top_{period}_{fb}'
    # items = items.filter(**{ field: True})
    if sort is not None:
        if direction == 'desc':
            direction = '-'
        else:
            direction = ''
        items = items.order_by(f'{direction}{sort}')
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


def export_queries(request):
    config = Config.objects(calculated=True).first()
    items = Queries.objects(
        # current_parsing_id=config.current_parsing_id,
        current_parsing_id=1672043096,
        root__ne=None
    )
    fields = ['Корень', 'Характеристики', 'Кол-во товаров',
              'Товары с продажами', 'Товары с продажами',
              'Оборот первого товара', 'Оборот десятого товара',
              'Средняя цена пред', 'Средняя цена тек', 'Изменение оборота',
              'Количество продавцов', 'Продавцы с продажами',
              'Продавцы с продажами', 'Топ', 'Топ товар 1', 'Топ товар 10',
              'Топ товары с продажами', 'Топ средний чек', 'Топ оборот']
    rows = [
        [i.root, i.features, i.products_count, i.products_with_sales,
         int((i.products_with_sales or 0) * 100 / i.products_count) if i.products_count else 0,
         i.first_product_hom_profit, i.ten_product_hom_profit,
         i.avg_price_prev_period, i.avg_price_period,
         int((i.avg_price_period or 0) * 100 / i.avg_price_prev_period) if i.avg_price_prev_period else 0,
         i.sellers, i.sellers_with_sales,
         int((i.sellers_with_sales or 0) * 100 / i.sellers) if i.sellers else 0,
         i.top, i.first_product_profit_top, i.ten_product_profit_top,
         i.products_with_sales_top, i.avg_price_top, i.profit_top]
        for i in items
    ]
    filename = f'{config.current_parsing_id}-queries.csv'
    file_path = f'export/{filename}'
    with open(file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    f = open(file_path, 'r')
    content = f.read()
    return Response(
        content,
        mimetype="text/csv",
        headers={
            "Content-disposition":
            f"attachment; filename={filename}"})


def export_categories():
    config = Config.objects(calculated=True).first()
    items = Categories.objects(parse=True).all()
    fields = ['Наименование', 'Кол-во товаров',
              'Товары с продажами', 'Товары с продажами',
              'Оборот первого товара', 'Оборот десятого товара',
              'Средняя цена пред', 'Средняя цена тек', 'Изменение оборота',
              'Количество продавцов', 'Продавцы с продажами',
              'Продавцы с продажами', 'Топ', 'Топ товар 1', 'Топ товар 10',
              'Топ товары с продажами', 'Топ средний чек', 'Топ оборот']
    rows = [
        [i.name, i.products_count, i.products_with_sales,
         int(i.products_with_sales * 100 / i.products_count) if i.products_count else 0,
         i.first_product_hom_profit, i.ten_product_hom_profit,
         i.avg_price_prev_period, i.avg_price_period,
         int(i.avg_price_period * 100 / i.avg_price_prev_period),
         i.sellers, i.sellers_with_sales,
         int(i.sellers_with_sales * 100 / i.sellers),
         i.top, i.first_product_profit_top, i.ten_product_profit_top,
         i.rel_sales_top, i.avg_price_top, i.profit_top]
        for i in items
    ]
    filename = f'{config.current_parsing_id}-categories.csv'
    file_path = f'export/{filename}'
    with open(file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    f = open(file_path, 'r')
    content = f.read()
    return Response(
        content,
        mimetype="text/csv",
        headers={
            "Content-disposition":
            f"attachment; filename={filename}"})


def get_child_ids(category, ids):
    for child in Categories.objects(parent=category.wb_id):
        ids.append(child.wb_id)
        get_child_ids(child, ids)
    return ids


def category(request, id):
    category_ = Categories.objects.get(pk=id)
    products = Products.objects(
        categories__in=[category_.wb_id]
    )
    sort = request.args.get('sort')
    if sort:
        products = products.order_by(f'-{sort}')
    else:
        products = products.order_by('-current_hom_profit')
    products = products[0:100]
    return {
        'category': json.loads(category_.to_json()),
        'products': json.loads(products.to_json()),
    }


def data(request):
    return {
        'products': json.loads(Products.objects.filter(to_sort=True, inner_rating__gt=0).order_by('-inner_rating').limit(30).to_json()),
        'totalPages': int(Products.objects.filter(to_sort=True, inner_rating__gt=0).count() / 30),
        'categories': json.loads(Categories.objects.to_json()),
    }


def products(request):
    page = int(request.GET.get('page'))
    skip = (page - 1) * 30
    products = Products.objects.filter(to_sort=True, inner_rating__gt=0).order_by('-inner_rating').skip(skip).limit(30)
    return {
        'products': json.loads(products.to_json()),
    }


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
