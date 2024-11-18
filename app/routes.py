from flask import jsonify, request
from app import db
from app.models import Product

def initialize_routes(app):
    @app.route('/')
    def home():
        return jsonify(message="Welcome to the E-commerce API")
    
    @app.route('/products', methods=['POST'])
    def add_product():
        data=request.json
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({"error" : "Invalid product data"}), 400
        
        product=Product(name=data['name'], price=data['price'])
        db.session.add(product)
        db.session.commit() #changes are committed

        return jsonify({"id": product.id, "name": product.name, "price": product.price}), 201


    @app.route('/products', methods=['GET'])
    def get_products():
        products=Product.query.all()
        product_list=[{"id": product.id, "name": product.name, "price" : product.price} for product in products]

        return jsonify(product_list)
    





        
