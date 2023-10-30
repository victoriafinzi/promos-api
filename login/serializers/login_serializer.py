from marshmallow import Schema, fields, post_load, pre_load, ValidationError
from flask import g
import bcrypt
from users.users import Users


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    user = fields.Nested('UsersSchema')
    access_token = fields.Str()

    @pre_load
    def prepare_object(self, data, **_):
        return data

    @post_load
    def make_object(self, data, **_):
        return data

    def validate_password(self, password, **kwargs):
        user = g.db_session.query(Users).filter(Users.username == self.context['username']).first()
        if not user:
            raise ValidationError("Invalid username or password")
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError("Invalid username or password")


class ResetPasswordSchema(Schema):
    password_reset_token = fields.Str(required=True)
    new_password = fields.Str(required=True, load_only=True)

    @pre_load
    def prepare_object(self, data, **_):
        return data

    @post_load
    def make_object(self, data, **_):
        return data
