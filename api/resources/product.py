"""Blueprint to organize and group, views related
to the '/products' endpoint of HTTP REST API.
"""
import json
from flask import (
    abort, Blueprint, request, Response, make_response, jsonify
)

from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from api.model import Product, ProductRepository
from api.model import UserRepository
from api.common.response import MakeResponse as makeResp

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/tree', methods=('GET',))
@jwt_required
def get_tree() -> Response:
    user_identity = get_jwt_identity()
    user = UserRepository().get_by_username(user_identity)

    response = None

    tree = ProductRepository().get_tree()
    if not tree:
        abort(404)

    else:
        response = makeResp.success(list(map(lambda prd: prd.serialize(), tree)))

    return response


@bp.route('', methods=('GET',))
@jwt_required
def get_products() -> Response:
    """get products.

       Returns:
           response: flask.Response object with the application/json mime-type.
       """

    user_identity = get_jwt_identity()
    user = UserRepository().get_by_username(user_identity)

    response = None

    products = ProductRepository().get_all_products()
    if not products:
        abort(404)

    else:
        response = makeResp.success(list(map(lambda prd: prd.serialize(), products)))

    return response
