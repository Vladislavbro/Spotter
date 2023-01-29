import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.forms.models import model_to_dict
from api.models import Customer


def me(request):
    if request.user.is_authenticated:
        user = User.objects.prefetch_related('customer').filter(
            pk=request.user.id).values(
                'id', 'username', 'email', 'first_name', 'last_name',
                'customer__subscribe_until', 'is_staff',
                'is_superuser').first()
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
                'customer__subscribe_until', 'is_staff',
                'is_superuser')
            return JsonResponse({'accounts': list(accounts)})
    return JsonResponse({'accounts': []})


def payment(request):
    # body = json.loads(request.body)
    print('payment')
    return HttpResponse('ok')
