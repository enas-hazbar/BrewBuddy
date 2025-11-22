from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=True)
    google_id = db.Column(db.String(255), unique=True)
    balance = db.Column(db.Float, default=0.0)

    # New fields
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)  # path to uploaded image
    role = db.Column(db.String(20), default="User") 


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    threshold = db.Column(db.Integer, default=5)
    price = db.Column(db.Float, default=0.0)

class Consumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    drink_id = db.Column(db.Integer, db.ForeignKey("drink.id"), nullable=False)
    amount = db.Column(db.Integer, default=1)
    date = db.Column(db.String(50))  

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey("drink.id"), nullable=False)
    quantity_needed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50))
    is_purchased = db.Column(db.Boolean, default=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))


