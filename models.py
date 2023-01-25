from mongoengine import (connect, Document, EmbeddedDocument, IntField,
                         StringField, ReferenceField, DateTimeField, ListField,
                         BooleanField, DictField, EmbeddedDocumentListField,
                         FloatField)
from datetime import datetime

connect(db='wb22')

# https://flask-httpauth.readthedocs.io/en/latest/


class Config(Document):
    current_parsing_date = DateTimeField()
    current_parsing_id = IntField()
    parsing_done = BooleanField()
    queries_done = BooleanField()
    queries_calculated = BooleanField()
    categories_calculated = BooleanField()
    products_calculated = BooleanField()
    calculated = BooleanField()
    meta = {
        'ordering': ['-current_parsing_id']
    }


class Queries(Document):
    category_id = ReferenceField('Categories')
    articuls = ListField(default=[])
    root = StringField()
    features = ListField(default=[])
    products_count = IntField()
    products_with_sales = IntField()
    first_product_decada_profit = IntField()
    ten_product_decada_profit = IntField()
    first_product_hom_profit = IntField()
    ten_product_hom_profit = IntField()
    # period
    avg_price_prev_period = IntField()
    avg_price_period = IntField()
    profit_prev_period = IntField()
    profit_period = IntField()
    sales_period = IntField()
    # period end
    sellers = IntField()
    sellers_with_sales = IntField()
    parsed_at = DateTimeField()
    last_parsed_page = IntField()
    current_parsing_id = IntField()
    calculated = BooleanField()
    top = BooleanField()
    ten_product_profit_top = BooleanField()
    first_product_profit_top = BooleanField()
    products_with_sales_top = BooleanField()
    profit_top = BooleanField()
    avg_price_top = BooleanField()
    rel_sales_top = BooleanField()
    meta = {
        'indexes': [
            'current_parsing_id',
        ],
    }


class Categories(Document):
    name = StringField(required=True)
    wb_id = IntField(required=True)
    parent = IntField()
    query = StringField()
    seo = StringField()
    shard = StringField()
    url = StringField(required=True)
    parse = BooleanField(default=False)
    parsed_at = DateTimeField()
    last_parsed_page_at = DateTimeField()
    last_parsed_page = IntField()
    start_parsing_at = DateTimeField()
    current_parsing_id = IntField()
    updated_at = DateTimeField()
    # period
    profit_period = IntField()
    profit_prev_period = IntField()
    sales_period = IntField()
    avg_price_prev_period = IntField()
    avg_price_period = IntField()
    # end period
    first_product_price = IntField()
    first_product_decada_sales = IntField()
    first_product_decada_profit = IntField()
    ten_product_price = IntField()
    ten_product_decada_sales = IntField()
    ten_product_decada_profit = IntField()
    products_count = IntField()
    products_with_sales = IntField()
    sellers = IntField()
    sellers_with_sales = IntField()
    rel_sellers = FloatField()
    rel_sales = FloatField()
    top = BooleanField()
    ten_product_profit_top = BooleanField()
    first_product_profit_top = BooleanField()
    profit_top = BooleanField()
    avg_price_top = BooleanField()
    rel_sales_top = BooleanField()
    calculated = BooleanField()
    products_calculated = BooleanField()

    meta = {
        'indexes': [
            'parsed_at',
        ],
    }


class Users(Document):
    telegram_id = IntField()
    last_name = StringField()
    first_name = StringField()
    username = StringField()
    created_at = DateTimeField()


class Sizes(EmbeddedDocument):
    quantity = IntField(required=True)
    sales = IntField()
    profit = IntField()
    price = IntField()
    date = DateTimeField(required=True)


class Products(Document):
    check_articul = BooleanField()
    articul = IntField(required=True)  # , unique=True
    name = StringField(required=True)
    root = StringField()
    entity = StringField()
    features = ListField(default=[])
    brand = StringField(required=True)
    brand_id = IntField(required=True)
    category_name = StringField(required=True)
    category_id = ReferenceField('Categories')
    category_wb_id = IntField()
    queries = ListField(default=[])
    categories = ListField(default=[])
    subject_id = IntField(required=True)
    rating = FloatField()
    feedbacks = IntField()
    data = DictField()
    is_new = BooleanField()
    price = IntField()
    priceU = IntField()
    quantity = IntField()
    sales = IntField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_parsing_id = IntField()
    parsed_at = DateTimeField()
    sizes = EmbeddedDocumentListField('Sizes')
    # current_week_sales = IntField()
    # last_week_sales = IntField()
    current_decada_sales = IntField()
    last_decada_sales = IntField()
    decada_sales_growth = IntField()
    current_decada_profit = IntField()
    last_decada_profit = IntField()
    decada_profit_growth = IntField()

    # hom - half of month - полмесяца
    current_hom_sales = IntField()
    last_hom_sales = IntField()
    hom_sales_growth = IntField()
    current_hom_profit = IntField()
    last_hom_profit = IntField()
    hom_profit_growth = IntField()

    meta = {
        'indexes': [
            'check_articul',
            'articul',
            'category_wb_id',
            'categories',
            'queries',
            'parsed_at',
            'root',
            'decada_sales_growth',
            'hom_sales_growth',
            '-sales',
            ('category_id', 'last_parsing_id'),
        ],
    }
