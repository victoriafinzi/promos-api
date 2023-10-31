from flask import abort
from flask_jwt_extended import jwt_required
from utils.decorators import (
    body,
    response,
    admin_user_required
)
from utils.send_message import send_message
from promos.models.promos_model import (
    create_promo,
    get_promo,
    get_all_promos,
    update_promo,
    delete_promo
)
from users.models.user_model import get_clients
from promos.serializers.promos_serializer import (
    PromosSchema
)
from flask_smorest import Blueprint


BLUEPRINT = Blueprint('promos', __name__, url_prefix='/promos')
promos_schema = PromosSchema()
promos_schemas = PromosSchema(many=True)


@BLUEPRINT.route("/", methods=["POST"])
@body(promos_schema)
@response(promos_schema)
@admin_user_required
@jwt_required()
def new_promo(data):
    try:
        promo = create_promo(data)
        clients = get_clients()
        for c in clients:
            send_message(promo.description, '+' + c.phone_number)
        return promo
    except Exception as e:
        abort(400, f"Failed to create promo: {str(e)}")


@BLUEPRINT.route("/<int:promo_id>", methods=["GET"])
@response(promos_schema)
def promo(promo_id: int):
    try: 
        check_user_id = get_promo(promo_id)
        if not check_user_id:
            return {"errors": f"Promo {promo_id} not found."}, 404
        else:
            return get_promo(promo_id)
    except Exception as e:
        abort(400, f"Failed to get promo {promo_id}: {str(e)}")


@BLUEPRINT.route("/", methods=["GET"])
@response(promos_schemas)
def all_promos():
    try:
        return get_all_promos()
    except Exception as e:
        abort(400, f"Failed to get all promos: {str(e)}")


@BLUEPRINT.route("/", methods=["PUT"])
@body(promos_schema)
@response(promos_schema)
@admin_user_required
@jwt_required()
def edit_promo(data):
    try: 
        check_promo = get_promo(data.id)
        print(check_promo, flush=True)
        if not check_promo:
            return {"errors": f"Promo {data.id} not found."}, 404
        else:
            update_promo(data)
            return {"message": f"Promo {data.id} edited successfully"}, 200
    except Exception as e:
        abort(400, f"Failed to update promo {data.id}: {str(e)}")
    

@BLUEPRINT.route("/<int:promo_id>", methods=["DELETE"])
@response(promos_schema)
@admin_user_required
@jwt_required()
def remove_promo(promo_id: int):
    try:
        check_promo = get_promo(promo_id)
        if not check_promo:
            return {"errors": f"Promo {promo_id} not found."}, 404
        else:
            delete_promo(promo_id)
            return {"message": f"User {promo_id} deleted successfully"}, 200
    except Exception as e:
        abort(500, f"Failed to delete user {promo_id}: {str(e)}")
