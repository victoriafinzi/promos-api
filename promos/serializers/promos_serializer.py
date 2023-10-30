from promos.promos import Promos
from marshmallow import (
    Schema,
    fields,
    post_load,
    pre_load,
    post_dump
)

class PromosSchema(Schema):

    class Meta:
        model = Promos
        ordered = True

    id = fields.Int()
    created_by = fields.Int(required=True, load_only=True)
    user = fields.Nested('UsersSchema', only=('id',), dump_only=True)
    product_name = fields.Str(required=True)
    price = fields.Float(required=True)
    discount = fields.Float(required=True)
    create_date = fields.Date()
    expiration_date = fields.Date(required=True)
    description = fields.Str()
    discounted_price = fields.Float()

    @pre_load
    def prepare_object(self, data, **_):
        return data
    
    @post_dump
    def add_discounted_price(self, data, **_):
        data['discounted_price'] = round(data['price'] * (1 - data['discount'] / 100), 2)
        return data

    @post_load
    def make_object(self, data, **_):
        return Promos(**data)
