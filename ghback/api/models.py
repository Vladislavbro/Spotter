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
    mongo_id = models.CharField(max_length=24, blank=True, null=True)
    thread_id = models.IntegerField(blank=True, null=True)
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
    mongo_id = models.CharField(max_length=24, blank=True, null=True)
    parsed_ids = ArrayField(ArrayField(models.IntegerField(blank=True)),
                            default=[])
    name = models.CharField(max_length=200)
    wb_id = models.IntegerField()
    parent = models.IntegerField(blank=True, null=True)
    wb_query = models.TextField(max_length=4000, blank=True, null=True)
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
    # period = models.IntegerField()
    # fb = models.CharField(max_length=3)
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


class Query(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)
    parsing_id = models.IntegerField(blank=True, null=True)
    root = models.CharField(max_length=200)
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

    # avg_price_prev_period = models.IntegerField(blank=True, null=True)
    # avg_price_period = models.IntegerField(blank=True, null=True)
    # profit_prev_period = models.BigIntegerField(blank=True, null=True)
    # profit_period = models.BigIntegerField(blank=True, null=True)
    # sales_period = models.IntegerField(blank=True, null=True)
    # sellers = models.IntegerField(blank=True, null=True)
    # sellers_with_sales = models.IntegerField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['-parsing_id'])
        ]


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 blank=True, null=True)
    articul = models.IntegerField()  # , unique=True
    # parsing_id = models.IntegerField(blank=True, null=True)
    parsed_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200)
    # desc = models.TextField()
    root = models.CharField(max_length=200)
    entity = models.CharField(max_length=200, blank=True, null=True)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    brand = models.CharField(max_length=200, blank=True, null=True)
    brand_id = models.IntegerField(blank=True, null=True)
    categories = ArrayField(ArrayField(models.IntegerField(blank=True)),
                            default=[])
    rating = models.FloatField(blank=True, null=True)
    feedbacks = models.IntegerField(blank=True, null=True)
    # is_new = models.BooleanField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    priceU = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta():
        indexes = [
            models.Index(fields=['articul']),
            models.Index(fields=['categories']),
            # models.Index(fields=['queries']),
            models.Index(fields=['parsed_at']),
            models.Index(fields=['root', 'features']),
            # models.Index(fields=['current_hom_sales']),
            # models.Index(fields=['hom_sales_growth']),
            # models.Index(fields=['-sales']),
            # models.Index(fields=['category_id', 'last_parsing_id']),
        ]


class ProductStat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parsing_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField()
    quantity_fbo = models.IntegerField(blank=True, null=True, default=0)
    quantity_fbs = models.IntegerField(blank=True, null=True, default=0)
    sales_fbo = models.IntegerField(blank=True, null=True, default=0)
    sales_fbs = models.IntegerField(blank=True, null=True, default=0)
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
    price = models.IntegerField(blank=True, null=True)
    priceU = models.IntegerField(blank=True, null=True)
    # price_7 = models.IntegerField()
    # priceU_7 = models.IntegerField()
    # price_14 = models.IntegerField()
    # priceU_14 = models.IntegerField()
    # price_30 = models.IntegerField()
    # priceU_30 = models.IntegerField()

    class Meta():
        ordering = ['-parsing_id']
        indexes = [
            # models.Index(fields=['-date']),
            models.Index(fields=['-parsing_id']),
            models.Index(fields=['-profit_30_fbo']),
        ]


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    quantity_fbo = models.IntegerField(blank=True, null=True, default=0)
    quantity_fbs = models.IntegerField(blank=True, null=True, default=0)
    sales = models.IntegerField(blank=True, null=True, default=0)
    # fulfilment by operator
    sales_fbo = models.IntegerField(blank=True, null=True, default=0)
    # fulfilment by seller
    sales_fbs = models.IntegerField(blank=True, null=True, default=0)
    profit = models.BigIntegerField(blank=True, null=True, default=0)
    profit_fbo = models.BigIntegerField(blank=True, null=True, default=0)
    profit_fbs = models.BigIntegerField(blank=True, null=True, default=0)
    price = models.IntegerField(blank=True, null=True, default=0)
    date = models.DateTimeField(blank=True, null=True)

    class Meta():
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]