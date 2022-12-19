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


class Queries(Document):
    category_id = ReferenceField('Categories')
    root = StringField()
    features = ListField(default=[])
    query_products_count = IntField()
    first_product_decada_profit = IntField()
    ten_product_decada_profit = IntField()
    products_with_sales = IntField()
    avg_price_prev_period = IntField()
    avg_price_period = IntField()
    profit_prev_period = IntField()
    profit_period = IntField()
    sellers = IntField()
    sellers_with_sales = IntField()
    sales_period = IntField()
    parsed_at = DateTimeField()
    last_parsed_page = IntField()


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
    meta = {
        'indexes': [
            'parsed_at',
        ],
    }


class Sizes(EmbeddedDocument):
    quantity = IntField(required=True)
    sales = IntField()
    profit = IntField()
    price = IntField()
    date = DateTimeField(required=True)


class Products(Document):
    articul = IntField(required=True)
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
    rating = IntField()
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
    last_decada_profit = IntField()
    current_decada_profit = IntField()
    meta = {
        'indexes': [
            'articul',
            'category_wb_id',
            'categories',
            'queries',
            'parsed_at',
            'root',
            'decada_sales_growth',
            '-sales',
            ('category_id', 'last_parsing_id'),
        ],
    }
