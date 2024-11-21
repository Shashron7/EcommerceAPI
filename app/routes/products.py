from flask import Blueprint, jsonify

products_blueprint=Blueprint('products', __name__)

@products_blueprint.route('/', methods=['GET'])
def get_all_products():
    return jsonify({"message" : "List of products"})