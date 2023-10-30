from users.users import Users, UserType
from marshmallow import (
    Schema,
    fields,
    post_load,
    pre_load
)
from utils.utils import hash_password


class UsersSchema(Schema):
    class Meta:
        model = Users
        ordered = True

    id = fields.Int()
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    username = fields.Str()
    password = fields.Str(load_only=True)
    user_type = fields.Method('serialize_user_type', deserialize='deserialize_user_type')
    password_reset_token = fields.Str(dump_only=True)
    password_reset_token_expiration = fields.DateTime(dump_only=True)

    @pre_load
    def prepare_object(self, data, **_):
        return data

    @post_load
    def make_object(self, data, **_):
        password = data.get('password')
        if password:
            data['password'] = hash_password(password)
        return Users(**data)

    def serialize_user_type(self, obj):
        if isinstance(obj, dict):
            return obj.get('user_type')
        elif isinstance(obj, Users):
            return obj.user_type.value
        return None

    def deserialize_user_type(self, value):
        if isinstance(value, int):
            return UserType(value)
        try:
            return UserType[value]
        except KeyError:
            raise ValueError(f"Invalid user_type value: {value}")
