from flask import Blueprint, jsonify

cart_blueprint = Blueprint('cart', __name__)

@cart_blueprint.route('/', methods=['GET'])
def get_cart():
    # Dummy response for now
    return jsonify({"message": "Cart details"})
