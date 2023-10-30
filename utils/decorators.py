from functools import wraps
from flask import request, Response, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from users.users import UserType
from users.models import user_model


def response(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                if type(result) == tuple and (result[0].get('message') or result[0].get('errors')):
                    return result
            except Exception:
                pass
            serialized_result = schema.dumps(result)
            return Response(serialized_result, mimetype="application/json")
        return wrapper
    return decorator


def body(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.is_json:
                    data = schema.load(request.json)
                elif 'multipart/form-data' in request.headers.get('content-type'):
                    data = schema.load(request.form)
                else:
                    raise ValidationError("The content-type for the request is not accepted.")

            except ValidationError as e:
                return {"errors": e.messages}, 422
            kwargs["data"] = data
            return func(*args, **kwargs)
        return wrapper
    return decorator


def admin_user_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = user_model.get_user(current_user_id)
        
        if user and user.user_type == UserType.ADMIN:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper
