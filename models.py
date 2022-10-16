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


class Categories(Document):
    name = StringField(required=True)
    wb_id = IntField(required=True)
    parent = IntField(required=True)
    query = StringField()
    seo = StringField()
    shard = StringField()
    url = StringField(required=True)
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
    date = DateTimeField(required=True)


class Products(Document):
    articul = IntField(required=True)
    name = StringField(required=True)
    brand = StringField(required=True)
    brand_id = IntField(required=True)
    category_name = StringField(required=True)
    category_id = ReferenceField('Categories')
    category_wb_id = IntField()
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
    meta = {
        'indexes': [
            'articul',
            'parsed_at',
            '-sales',
            ('category_id', 'last_parsing_id'),
        ],
    }
