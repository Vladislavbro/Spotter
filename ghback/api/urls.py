from django.urls import path

from . import views

urlpatterns = [
    path('auth/me', views.me, name='me'),
    path('auth/log_in', views.log_in, name='log_in'),
    path('auth/log_out', views.log_out, name='log_out'),
    path('auth/signup', views.signup, name='signup'),
    path('payment', views.payment, name='payment'),
    path('accounts', views.accounts, name='accounts'),
    path('account', views.account, name='account'),
]
