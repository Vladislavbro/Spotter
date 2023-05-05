from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, HStoreField

# Create your models here.

# class Users(Document):
#     telegram_id = IntField()
#     last_name = StringField()
#     first_name = StringField()
#     username = StringField()
#     created_at = DateTimeField()


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
    # period
    profit_period = models.BigIntegerField(blank=True, null=True)
    profit_prev_period = models.BigIntegerField(blank=True, null=True)
    sales_period = models.BigIntegerField(blank=True, null=True)
    avg_price_prev_period = models.IntegerField(blank=True, null=True)
    avg_price_period = models.IntegerField(blank=True, null=True)
    # end period
    first_product_price = models.IntegerField(blank=True, null=True)
    first_product_sales = models.IntegerField(blank=True, null=True)
    first_product_profit = models.BigIntegerField(blank=True, null=True)
    ten_product_price = models.IntegerField(blank=True, null=True)
    ten_product_sales = models.IntegerField(blank=True, null=True)
    ten_product_profit = models.BigIntegerField(blank=True, null=True)
    products_count = models.IntegerField(blank=True, null=True)
    products_with_sales = models.IntegerField(blank=True, null=True)
    sellers = models.IntegerField(blank=True, null=True)
    sellers_with_sales = models.IntegerField(blank=True, null=True)
    rel_sellers = models.FloatField(blank=True, null=True)
    rel_sales = models.FloatField(blank=True, null=True)
    top = models.BooleanField(blank=True, null=True)
    ten_product_profit_top = models.BooleanField(blank=True, null=True)
    first_product_profit_top = models.BooleanField(blank=True, null=True)
    profit_top = models.BooleanField(blank=True, null=True)
    avg_price_top = models.BooleanField(blank=True, null=True)
    rel_sales_top = models.BooleanField(blank=True, null=True)
    calculated = models.BooleanField(blank=True, null=True)
    products_calculated = models.BooleanField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['parsed_at'])
        ]


class Query(models.Model):
    mongo_id = models.CharField(max_length=30, blank=True, null=True)
    mongo_category_id = models.CharField(max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)
    # category_id = ReferenceField('Categories')
    articuls = ArrayField(ArrayField(models.IntegerField(blank=True)),
                          default=[])
    root = models.CharField(max_length=200)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    products_count = models.IntegerField(blank=True, null=True)
    products_with_sales = models.IntegerField(blank=True, null=True)
    rel_products_with_sales = models.IntegerField(blank=True, null=True)
    first_product_hom_profit = models.BigIntegerField(blank=True, null=True)
    ten_product_hom_profit = models.BigIntegerField(blank=True, null=True)
    avg_price_prev_period = models.IntegerField(blank=True, null=True)
    avg_price_period = models.IntegerField(blank=True, null=True)
    profit_prev_period = models.BigIntegerField(blank=True, null=True)
    profit_period = models.BigIntegerField(blank=True, null=True)
    sales_period = models.IntegerField(blank=True, null=True)
    sellers = models.IntegerField(blank=True, null=True)
    sellers_with_sales = models.IntegerField(blank=True, null=True)
    parsed_at = models.DateTimeField(blank=True, null=True)
    last_parsed_page = models.IntegerField(blank=True, null=True)
    current_parsing_id = models.IntegerField(blank=True, null=True)
    calculated = models.BooleanField(blank=True, null=True)
    top = models.BooleanField(blank=True, null=True)
    ten_product_profit_top = models.BooleanField(blank=True, null=True)
    first_product_profit_top = models.BooleanField(blank=True, null=True)
    products_with_sales_top = models.BooleanField(blank=True, null=True)
    profit_top = models.BooleanField(blank=True, null=True)
    avg_price_top = models.BooleanField(blank=True, null=True)
    rel_sales_top = models.BooleanField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['current_parsing_id'])
        ]


class Product(models.Model):
    mongo_id = models.CharField(max_length=24, blank=True, null=True)
    mongo_transfered = models.BooleanField(default=False, blank=True,
                                           null=True)
    # mongo_category_id = models.CharField(max_length=24, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 blank=True, null=True)
    articul = models.IntegerField()  # , unique=True
    name = models.CharField(max_length=200)
    root = models.CharField(max_length=200)
    entity = models.CharField(max_length=200, blank=True, null=True)
    features = ArrayField(ArrayField(models.CharField(max_length=100,
                                                      blank=True)), default=[])
    brand = models.CharField(max_length=200, blank=True, null=True)
    brand_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=200)
    category_wb_id = models.IntegerField(blank=True, null=True)
    # queries = ArrayField(ArrayField(models.IntegerField(blank=True)),
    #                      default=[])
    categories = ArrayField(ArrayField(models.IntegerField(blank=True)),
                            default=[])
    subject_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    feedbacks = models.IntegerField(blank=True, null=True)
    is_new = models.BooleanField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    priceU = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    quantity_fbo = models.IntegerField(blank=True, null=True)
    quantity_fbs = models.IntegerField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)
    sales_fbo = models.IntegerField(blank=True, null=True)
    sales_fbs = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_parsing_id = models.IntegerField(blank=True, null=True)
    parsed_at = models.DateTimeField(blank=True, null=True)
    current_hom_sales = models.IntegerField(blank=True, null=True)
    last_hom_sales = models.IntegerField(blank=True, null=True)
    hom_sales_growth = models.IntegerField(blank=True, null=True)
    current_hom_profit = models.BigIntegerField(blank=True, null=True)
    last_hom_profit = models.BigIntegerField(blank=True, null=True)
    hom_profit_growth = models.IntegerField(blank=True, null=True)

    class Meta():
        indexes = [
            models.Index(fields=['articul']),
            models.Index(fields=['categories']),
            # models.Index(fields=['queries']),
            models.Index(fields=['parsed_at']),
            models.Index(fields=['root', 'features']),
            models.Index(fields=['current_hom_sales']),
            # models.Index(fields=['hom_sales_growth']),
            models.Index(fields=['-sales']),
            # models.Index(fields=['category_id', 'last_parsing_id']),
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
