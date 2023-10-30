from flask import abort
from flask_jwt_extended import jwt_required
from users.users import UserType
from utils.decorators import (
    body,
    response
)
from users.models.user_model import (
    create_user,
    get_user,
    update_user,
    delete_user
)
from users.serializers.user_serializer import (
    UsersSchema
)
from flask_smorest import Blueprint


BLUEPRINT = Blueprint('users', __name__, url_prefix='/users')
user_schema = UsersSchema()


@BLUEPRINT.route("/", methods=["POST"])
@body(user_schema)
@response(user_schema)
def new_user(data):
    try:
        return create_user(data)
    except Exception as e:
        abort(400, f"Failed to create user: {str(e)}")


@BLUEPRINT.route("/<int:user_id>", methods=["GET"])
@response(user_schema)
@jwt_required()
def user(user_id: int):
    try: 
        check_user_id = get_user(user_id)
        if not check_user_id:
            return {"errors": f"User {user_id} not found."}, 404
        else:
            return get_user(user_id)
    except Exception as e:
        abort(400, f"Failed to get user {user_id}: {str(e)}")


@BLUEPRINT.route("/", methods=["PUT"])
@body(user_schema)
@response(user_schema)
@jwt_required()
def alter_user(data):
    try: 
        check_user = get_user(data.id)
        if not check_user:
            return {"errors": f"User {data.id} not found."}, 404
        else:
            update_user(data)
            return {"message": f"User {data.id} edited successfully"}, 200
    except Exception as e:
        abort(400, f"Failed to update user {data.id}: {str(e)}")
    

@BLUEPRINT.route("/<int:user_id>", methods=["DELETE"])
@response(user_schema)
@jwt_required()
def remove_user(user_id: int):
    try:
        check_user = get_user(user_id)
        if not check_user:
            return {"errors": f"User {user_id} not found."}, 404
        else:
            delete_user(user_id)
            return {"message": f"User {user_id} deleted successfully"}, 200
    except Exception as e:
        abort(500, f"Failed to delete user {user_id}: {str(e)}")
