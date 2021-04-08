from flask import Flask, render_template, request, redirect, url_for
from configs.base_config import Development, Staging, Production
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flaskinventory'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # db.drop_all()

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    item_name = db.Column(db.String(80), unique=False, nullable=False)
    item_quantity = db.Column(db.Integer, unique=False)
    item_buying_price = db.Column(db.Integer, unique=False)
    item_selling_price = db.Column(db.Integer, unique=False)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, unique=False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    item = db.relationship('Item',
        backref=db.backref('sales', lazy=True))

@app.route('/', methods = ['GET', 'POST'])
def itemlisting():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_quantity = request.form['item_quantity']
        item_buying_price = request.form['item_buying_price']
        item_selling_price = request.form['item_selling_price']

        a = Item(item_name = item_name, item_quantity = item_quantity, item_buying_price = item_buying_price, item_selling_price = item_selling_price)
        db.session.add(a)
        db.session.commit()
        print("Record successfully added")
        
        return redirect(url_for('itemlisting'))
        
    items = Item.query.all()
    return render_template('items.html', items = items)

@app.route('/sales', methods = ['POST'])
def saleslisting():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['item_quantity']
        print("mama", item_id, quantity)

        a = Sale(item_id = item_id, quantity = quantity)
        db.session.add(a)
        db.session.commit()
        print("Record successfully added")
        
        return redirect(url_for('itemlisting'))

if __name__ == '__main__':
    app.run(debug = True)