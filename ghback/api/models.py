from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True, null=True)
    subscribe_type = models.CharField(max_length=100, blank=True, null=True)
    subscribe_until = models.IntegerField(blank=True, null=True)

    def __str__(self):
        user = self.user
        return '{0} {1}'.format(user.first_name, user.last_name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    subscribe_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        user = self.user
        return '{0} {1} {2}'.format(user.first_name, user.last_name, self.date)


class Config(models.Model):
    thread_id = models.IntegerField(blank=True, null=True)
    baskets_thread_id = models.IntegerField(blank=True, null=True)
    parsing_date = models.BigIntegerField(blank=True, null=True)
    current_parsing_id = models.IntegerField(blank=True, null=True)
    parsed_at = models.DateTimeField(blank=True, null=True)
    parsing_done = models.BooleanField(default=False)
    queries_done = models.BooleanField(default=False)
    queries_calculated = models.BooleanField(default=False)
    categories_calculated = models.BooleanField(default=False)
    products_calculated = models.BooleanField(default=False)
    calculated = models.BooleanField(default=False)

    class Meta():
        ordering = ['-current_parsing_id']


class Category(models.Model):
    parsed_ids = ArrayField(ArrayField(models.IntegerField(blank=True)),
                            default=[])
    first_product = models.ForeignKey(
        'Product', on_delete=models.DO_NOTHING, blank=True, null=True, 
        related_name='first_product_category')
    name = models.CharField(max_length=200)
    wb_id = models.IntegerField()
    parent = models.IntegerField(blank=True, null=True)
    wb_query = models.TextField(max_length=4000, blank=True, null=True)
    idx = models.IntegerField(blank=True, null=True)
    seo = models.CharField(max_length=200, blank=True, null=True)
    shard = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    parse = models.BooleanField(default=False)
    parsed_at = models.DateTimeField(blank=True, null=True)
    last_parsed_page_at = models.DateTimeField(blank=True, null=True)
    last_parsed_page = models.IntegerField(blank=True, null=True)
    start_parsing_at = models.DateTimeField(blank=True, null=True)
    current_parsing_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    products_calculated = models.BooleanField(blank=True, null=True)
    calculated = models.BooleanField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['-parsed_at'])
        ]


class CategoryStat(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    parsing_id = models.IntegerField(blank=True, null=True)
    scoring = models.JSONField(blank=True, null=True)
    products_count = models.IntegerField(blank=True, null=True)
    products_solded_7_fbo = models.IntegerField(blank=True, null=True)
    products_solded_7_fbs = models.IntegerField(blank=True, null=True)
    products_solded_14_fbo = models.IntegerField(blank=True, null=True)
    products_solded_14_fbs = models.IntegerField(blank=True, null=True)
    products_solded_30_fbo = models.IntegerField(blank=True, null=True)
    products_solded_30_fbs = models.IntegerField(blank=True, null=True)
    sellers_count_7 = models.IntegerField(blank=True, null=True)
    sellers_count_14 = models.IntegerField(blank=True, null=True)
    sellers_count_30 = models.IntegerField(blank=True, null=True)
    sellers_solded_7_fbo = models.IntegerField(blank=True, null=True)
    sellers_solded_7_fbs = models.IntegerField(blank=True, null=True)
    sellers_solded_14_fbo = models.IntegerField(blank=True, null=True)
    sellers_solded_14_fbs = models.IntegerField(blank=True, null=True)
    sellers_solded_30_fbo = models.IntegerField(blank=True, null=True)
    sellers_solded_30_fbs = models.IntegerField(blank=True, null=True)
    profit_7_fbo = models.BigIntegerField(blank=True, null=True)
    profit_7_fbs = models.BigIntegerField(blank=True, null=True)
    profit_14_fbo = models.BigIntegerField(blank=True, null=True)
    profit_14_fbs = models.BigIntegerField(blank=True, null=True)
    profit_30_fbo = models.BigIntegerField(blank=True, null=True)
    profit_30_fbs = models.BigIntegerField(blank=True, null=True)
    price_avg_7 = models.IntegerField(blank=True, null=True)
    price_avg_14 = models.IntegerField(blank=True, null=True)
    price_avg_30 = models.IntegerField(blank=True, null=True)
    top_7_fbo = models.BooleanField(blank=True, null=True)
    top_7_fbs = models.BooleanField(blank=True, null=True)
    top_14_fbo = models.BooleanField(blank=True, null=True)
    top_14_fbs = models.BooleanField(blank=True, null=True)
    top_30_fbo = models.BooleanField(blank=True, null=True)
    top_30_fbs = models.BooleanField(blank=True, null=True)

    class Meta():
        ordering = ['-parsing_id']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 blank=True, null=True)
    articul = models.IntegerField()  # , unique=True
    basket = models.IntegerField(blank=True, null=True)
    # parsing_id = models.IntegerField(blank=True, null=True)
    parsed_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200)
    # desc = models.TextField()
    lemmas = ArrayField(ArrayField(
        models.CharField(max_length=100, blank=True)), default=[])
    root = models.CharField(max_length=200)
    entity = models.CharField(max_length=200, blank=True, null=True)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    brand = models.CharField(max_length=200, blank=True, null=True)
    brand_id = models.IntegerField(blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    categories = ArrayField(ArrayField(models.IntegerField(blank=True)),
                            default=[])
    rating = models.FloatField(blank=True, null=True)
    feedbacks = models.IntegerField(blank=True, null=True)
    # is_new = models.BooleanField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    priceU = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta():
        indexes = [
            models.Index(fields=['lemmas']),
            models.Index(fields=['articul']),
            models.Index(fields=['categories']),
            models.Index(fields=['parsed_at']),
            models.Index(fields=['root', 'features']),
            models.Index(fields=['basket']),
            models.Index(fields=['supplier_id']),
        ]


class Query(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)
    first_product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                      blank=True, null=True)
    parsing_id = models.IntegerField(blank=True, null=True)
    root = models.CharField(max_length=200)
    scoring = models.JSONField(blank=True, null=True)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    products_count = models.IntegerField(blank=True, null=True)
    products_solded_7_fbo = models.IntegerField(blank=True, null=True)
    products_solded_7_fbs = models.IntegerField(blank=True, null=True)
    products_solded_14_fbo = models.IntegerField(blank=True, null=True)
    products_solded_14_fbs = models.IntegerField(blank=True, null=True)
    products_solded_30_fbo = models.IntegerField(blank=True, null=True)
    products_solded_30_fbs = models.IntegerField(blank=True, null=True)
    product_1_profit_7_fbo = models.BigIntegerField(blank=True, null=True)
    product_1_profit_7_fbs = models.BigIntegerField(blank=True, null=True)
    product_1_profit_14_fbo = models.BigIntegerField(blank=True, null=True)
    product_1_profit_14_fbs = models.BigIntegerField(blank=True, null=True)
    product_1_profit_30_fbo = models.BigIntegerField(blank=True, null=True)
    product_1_profit_30_fbs = models.BigIntegerField(blank=True, null=True)
    product_10_profit_7_fbo = models.BigIntegerField(blank=True, null=True)
    product_10_profit_7_fbs = models.BigIntegerField(blank=True, null=True)
    product_10_profit_14_fbo = models.BigIntegerField(blank=True, null=True)
    product_10_profit_14_fbs = models.BigIntegerField(blank=True, null=True)
    product_10_profit_30_fbo = models.BigIntegerField(blank=True, null=True)
    product_10_profit_30_fbs = models.BigIntegerField(blank=True, null=True)
    price_avg_7 = models.IntegerField(blank=True, null=True)
    price_avg_14 = models.IntegerField(blank=True, null=True)
    price_avg_30 = models.IntegerField(blank=True, null=True)
    profit_7_fbo = models.BigIntegerField(blank=True, null=True)
    profit_7_fbs = models.BigIntegerField(blank=True, null=True)
    profit_14_fbo = models.BigIntegerField(blank=True, null=True)
    profit_14_fbs = models.BigIntegerField(blank=True, null=True)
    profit_30_fbo = models.BigIntegerField(blank=True, null=True)
    profit_30_fbs = models.BigIntegerField(blank=True, null=True)
    top_7_fbo = models.BooleanField(blank=True, null=True)
    top_7_fbs = models.BooleanField(blank=True, null=True)
    top_14_fbo = models.BooleanField(blank=True, null=True)
    top_14_fbs = models.BooleanField(blank=True, null=True)
    top_30_fbo = models.BooleanField(blank=True, null=True)
    top_30_fbs = models.BooleanField(blank=True, null=True)
    calculated = models.BooleanField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['-parsing_id'])
        ]


class Supplier(models.Model):
    wb_id = models.IntegerField()
    name = models.CharField(max_length=200)
    inn = models.CharField(max_length=100, blank=True, null=True)
    ogrn = models.CharField(max_length=100, blank=True, null=True)
    ogrnip = models.CharField(max_length=100, blank=True, null=True)
    trademark = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta():
        indexes = [
            models.Index(fields=['wb_id']),
        ]


class ProductStat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parsing_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField()
    quantity_fbo = models.IntegerField(blank=True, null=True, default=0)
    quantity_fbs = models.IntegerField(blank=True, null=True, default=0)
    sales_fbo = models.IntegerField(blank=True, null=True, default=0)
    sales_fbs = models.IntegerField(blank=True, null=True, default=0)
    profit_lost_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_lost_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    sales_7_fbo = models.IntegerField(blank=True, null=True, default=0)
    sales_7_fbs = models.IntegerField(blank=True, null=True, default=0)
    sales_14_fbo = models.IntegerField(blank=True, null=True, default=0)
    sales_14_fbs = models.IntegerField(blank=True, null=True, default=0)
    sales_30_fbo = models.IntegerField(blank=True, null=True, default=0)
    sales_30_fbs = models.IntegerField(blank=True, null=True, default=0)
    profit_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    profit_7_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_7_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    profit_14_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_14_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    profit_30_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_30_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    profit_30_fbo_grow = models.IntegerField(blank=True, null=True, default=0)
    price = models.IntegerField(blank=True, null=True)
    priceU = models.IntegerField(blank=True, null=True)

    class Meta():
        ordering = ['-date']
        indexes = [
            models.Index(fields=['parsing_id', 'product_id']),
        ]


class FboProfit30(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField()
    supplier_id = models.IntegerField(null=True)
    parsing_id = models.IntegerField()
    profit_30_fbo = models.DecimalField(max_digits=10, decimal_places=2)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    root = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'view_fbo_profit_30'