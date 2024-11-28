from app import db
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.Integer, nullable=False, unique=True)
    email=db.Column(db.String(120), nullable=False, unique=True)
    password=db.Column(db.String(128), nullable=False)


    # def set_password(self, password):
    #     self.password=bcrypt.generate_password_hash(password).decode('utf-8')

    # def check_password(self, password):
    #     return bcrypt.check_password_hash(self.password, password)


class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    description=db.Column(db.Text, nullable=True)
    price= db.Column(db.Float,  nullable=False)
    stock=db.Column(db.Integer, nullable=False)

    # a function to disp the product's data
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'description': self.description if self.description else None
        }


class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    items=db.relationship('CartItem', backref='cart', lazy=True)


class CartItem(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    cart_id=db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity=db.Column(db.Integer, nullable=False)




# When you define a model in SQLAlchemy, the table name is automatically inferred from the class name by converting it to lowercase, unless explicitly specified otherwise via the __tablename__ attribute.