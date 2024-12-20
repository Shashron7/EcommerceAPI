from flask import Blueprint, jsonify, session, request
from app.models import Cart, CartItem, Product, User, Order
from app import db
from app.utils import login_required
from datetime import datetime

cart_blueprint = Blueprint('cart', __name__)

#Login required for authorized access only

@cart_blueprint.route('', methods=['GET'])
@login_required
def get_cart_items():
    
    user_id=session['user_id']
    #finding cart of user
    cart=Cart.query.filter_by(user_id=user_id).first()
    if not cart:  #if not present show empty cart
        return jsonify({"message" : "Empty cart"})
    
    #Query those items that have the same cart id 
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()
    cart_data = []
    for item in cart_items:
        cart_data.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity
        })

    return jsonify({"cart_items": cart_data}), 200






@cart_blueprint.route('/add', methods=['POST'])
@login_required    
def add_to_cart():
    
    user_id=session['user_id'] #getting user data from session
    data=request.get_json()
    print('user_id is ', user_id)
    product_id=data.get('product_id')
    quantity=data.get('quantity', 1) #default is 1

    if not product_id:
        return jsonify({"message" : "Product ID is required"}), 400
    
    #Checking if the product exists
    product=Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    #Find users cart else we will create it

    cart=Cart.query.filter_by(user_id=user_id).first()

    if not cart: #if no cart present create one 
        cart=Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    
    #Check if the  cart item is already present or not in the cart
    cart_item=CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

    #if cartitem is present we increase the quantity
    if cart_item:
        cart_item.quantity+=quantity
    
    else:
        cart_item=CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()

    return jsonify({
        "message": "Product added to cart successfully.",
        "cart_item": {
            "id": cart_item.id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }
    }), 200


@cart_blueprint.route('/remove', methods=['DELETE'])
@login_required
def remove_from_cart():
    user_id=session['user_id']
    data=request.get_json()
    product_id=data.get('product_id')
    if not product_id:
        return jsonify({"error" : "Product ID is required"}), 400
    
    cart=Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({"message" : "Cart is empty"}), 404
    
    #Find the item in the cart

    cart_item=CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

    if not cart_item:
        return jsonify({"message" : "Product not found in cart"}), 404
    
    db.session.delete(cart_item)
    db.session.commit()


    return jsonify({"message" : "Product removed from cart successfully"})
    



@cart_blueprint.route('/summary', methods=['GET'])
@login_required
def summarise():
    user_id=session['user_id']
    cart=Cart.query.filter_by(user_id=user_id).first() #get the cart from the user id
    if not cart:
        return jsonify({"message": "Cart is empty"}), 400
    
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()

    cart_data =[]

    total_cost=0
    for item in cart_items:
        product=Product.query.get(item.product_id)
        if not product :
            continue

        item_total=product.price*item.quantity
        total_cost+=item_total

        cart_data.append(
            {
                "Product Name" : product.name,
                "Quantity" : item.quantity,
                "Price per Unit" : product.price, 
                "Total Price" : item_total
            }
        )

    
    return jsonify({"Cart Summary" : cart_data, "Total Cost" : total_cost}), 200
    

@cart_blueprint.route('checkout', methods=['GET'])
@login_required
def checkout():
    user_id=session['user_id']
    
    user = User.query.get(user_id)
    cart=Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({"message" : "Cart is empty"}), 404
    
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()

    total_cost=0
    for item in cart_items:
        curr_prod=Product.query.get(item.product_id)
        total_cost += curr_prod.price * item.quantity

        order =Order(
            user_id=user_id,
            product_id=curr_prod.id,
            quantity=item.quantity,
            total_price=item.quantity * curr_prod.price,
            purchase_date=datetime.utcnow()
        )

        db.session.add(order)

        



    if user.wallet_balance < total_cost :
        return jsonify({"Message" : "Insufficient Balance, add funds to your wallet"}), 400
    

    user.wallet_balance-=total_cost
    db.session.commit() #commiting changes

    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    
    
    return jsonify({
        "message": "Payment successful",
        "remaining_balance": user.wallet_balance
    }), 200
    
    


@cart_blueprint.route('/history', methods=['GET'])
@login_required
def order_history():
    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).all()

    if not orders:
        return jsonify({"message": "No purchase history found"}), 404

    order_data = []
    for order in orders:
        product = Product.query.get(order.product_id)
        order_data.append({
            "Product Name": product.name if product else "Unknown Product",
            "Quantity": order.quantity,
            "Total Price": order.total_price,
            "Purchase Date": order.purchase_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"Purchase History": order_data}), 200


