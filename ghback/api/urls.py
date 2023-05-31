from django.urls import path

from . import views

urlpatterns = [
    path('auth/me', views.me, name='me'),
    path('auth/log_in', views.log_in, name='log_in'),
    path('auth/log_out', views.log_out, name='log_out'),
    path('auth/signup', views.signup, name='signup'),
    path('payment', views.payment, name='payment'),
    path('order', views.order, name='order'),
    path('accounts', views.accounts, name='accounts'),
    path('account', views.account, name='account'),
    path('account/<int:id>/delete', views.delete_account,
         name='delete_account'),
    path('parser', views.parser, name='parser'),
    path('categories', views.categories_list, name='categories_list'),
    path('queries/top', views.queries_top, name='queries_top'),
    path('queries/search', views.queries_search, name='queries_search'),
    path('products/<int:articul>', views.product, name='product'),
    path('transfer/config', views.transfer_config, name='transfer_config'),
    path('transfer/category', views.transfer_category, name='transfer_category'),
    path('transfer/query', views.transfer_query, name='transfer_query'),
    path('transfer/product', views.transfer_product, name='transfer_product'),
]
