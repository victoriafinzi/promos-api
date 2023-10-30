from utils.decorators import (
    body, 
    response
)
from login.models.login_model import (
    validate_login, 
    generate_reset_token, 
    find_user_by_reset_token, 
    is_reset_token_expired
)
from users.models.user_model import (
    update_user,
    get_user
)
from login.serializers.login_serializer import ( 
    LoginSchema, 
    ResetPasswordSchema
)
from users.serializers.user_serializer import UsersSchema
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint
from utils.utils import hash_password

BLUEPRINT = Blueprint('login', __name__, url_prefix='/login')
login_schema = LoginSchema()
users_schema = UsersSchema()
reset_password_schema = ResetPasswordSchema()


@BLUEPRINT.route("/", methods=["POST"])
@body(login_schema)
@response(login_schema)
def login(data):
    username = data.get('username')
    password = data.get('password')

    user = validate_login(username, password)

    if user:
        access_token = create_access_token(identity=user.id)
        serialized_user = users_schema.dump(user)

        response_data = {
            "user": serialized_user,
            "access_token": access_token
        }

        return response_data
    else:
        return {"error": "Invalid username or password"}, 401


@BLUEPRINT.route("/generate-reset-token/<int:user_id>", methods=["POST"])
def generate_reset_token_route(user_id: int):
    user = get_user(user_id)

    if user:
        reset_token = generate_reset_token(user)

        return {"message": f"Reset token {reset_token} sent successfully"}, 200
    else:
        return {"error": "User not found"}, 404


@BLUEPRINT.route("/reset-password", methods=["POST"])
@body(reset_password_schema)
@response(reset_password_schema)
def reset_password(data):
    password_reset_token = data.get('password_reset_token')
    new_password = data.get('new_password')

    user = find_user_by_reset_token(password_reset_token)
    
    if user and not is_reset_token_expired(user.id):
        user.password = hash_password(new_password)
        user.password_reset_token = None
        user.password_reset_token_expiration = None
        update_user(user)
        return {"message: Password successfully reset"}, 200
    else:
        return {"errors: Invalid or expired reset token"}, 404
