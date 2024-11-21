from flask import Blueprint

#Importing blueprints from each file

from .products import products_blueprint
from .users import users_blueprint
from .cart import cart_blueprint


def initialize_routes(app):
    app.register_blueprint(products_blueprint, url_prefix="/products")
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(cart_blueprint, url_prefix="/cart")



