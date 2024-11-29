from flask import Blueprint, jsonify, request
from app.models import Product, db
from app.utils import login_required 
from flask import session



products_blueprint=Blueprint('products', __name__) #defining the blueprint of the product

@products_blueprint.route('', methods=['POST'])
def add_product():
    data = request.json
    name=data.get('name')
    price=data.get('price')
    stock=data.get('stock')
    description=data.get('description')

    if not name or not price or not stock:
        return jsonify({'error': 'Missing fields'}), 400
    


    new_product=Product(name=name, price=price, stock=stock, description=description)
    db.session.add(new_product)
    db.session.commit()



    return jsonify({'message': 'Product added successfully'}), 201

@products_blueprint.route('', methods=['GET'])
@login_required
def get_all_products():
    print("Session Data:", session)
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200



@products_blueprint.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product=Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(product.to_dict())

@products_blueprint.route('<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product=Product.query.get(product_id)
    if not product:
        return jsonify({'error' : 'Product not found'}), 404
    
    data=request.json
    product.name=data.get('name', product.name)
    product.price=data.get('price',product.price)
    product.stock=data.get('stock', product.stock)

    db.session.commit()

    return jsonify({'message' : 'Product updated successfully'}), 200

@products_blueprint.route('<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product=Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({'messsage' : 'Product deleted successfully'}), 200



