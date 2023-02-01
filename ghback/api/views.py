import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.forms.models import model_to_dict
from api.models import Customer, Order
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta


def me(request):
    if request.user.is_authenticated:
        user = User.objects.prefetch_related('customer').filter(
            pk=request.user.id).values(
                'id', 'username', 'email', 'first_name', 'last_name',
                'customer__subscribe_type', 'customer__subscribe_until',
                'is_staff', 'is_superuser').first()
        return JsonResponse(user)
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
