from flask import Flask, render_template, request, redirect, url_for
from configs.base_config import Development, Staging, Production
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pygal
# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Production) # comment new comment
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flaskinventory'
db = SQLAlchemy(app)
# login_manager = LoginManager(app)

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
    item_status = db.Column(db.Integer, unique=False)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), autoincrement = True)
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
        print(item_id, quantity)

        item_to_edit = Item.query.filter_by(id = item_id).first()
        item_to_edit.item_quantity = int(item_to_edit.item_quantity) - int(quantity)

        if int(item_to_edit.item_quantity) < 0:
            print("Quantity entered is more than the stock available")
            return redirect(url_for('itemlisting'))

        db.session.add(item_to_edit)
        db.session.commit()        

        a = Sale(item_id = item_id, quantity = quantity)
        db.session.add(a)
        db.session.commit()
        print("Record successfully added")
        
        return redirect(url_for('itemlisting'))

@app.route('/sale/<int:x>', methods = ['GET'])
def itemsales(x):
    if request.method == 'GET':
        item_sales = Sale.query.filter_by(item_id = x).all()
        print(item_sales)

        return render_template('sales.html', items = item_sales)

@app.route('/<int:y>/edit', methods = ['GET', 'POST'])
def edit_item(y):
    if request.method == 'GET':
        item_to_edit = Item.query.filter_by(id = y).first()
        print(item_to_edit)

        return render_template('inventory_edit.html', item = item_to_edit)
    else:
        item_to_edit = Item.query.filter_by(id = y).first()
        item_to_edit.item_name = request.form['item_name']
        item_to_edit.item_quantity = request.form['item_quantity']
        item_to_edit.item_buying_price = request.form['item_buying_price']
        item_to_edit.item_selling_price = request.form['item_selling_price']

        db.session.add(item_to_edit)
        db.session.commit()
        print("Record successfully edited")
        
        return redirect(url_for('itemlisting'))

@app.route('/charting')
def charting():
    sales = Sale.query.all()

    inv_dict = {}

    for i in sales:
        date_str =  i.created_at.strftime("%m-%d-%Y")
        if date_str in inv_dict.keys(): 
            inv_dict[date_str] =  inv_dict[date_str] + i.quantity
        else:
            inv_dict[date_str] = i.quantity

    bar_chart = pygal.Bar()
    bar_chart.title = "Sales made on different days"
    bar_chart.x_labels = map(str, inv_dict.keys())
    bar_chart.add('Value of Sales', inv_dict)
    chart = bar_chart.render(is_unicode=True)

    return render_template("charting.html", chart = chart)

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    item_to_delete = Item.query.get_or_404(id)

    db.session.delete(item_to_delete)
    db.session.commit()

    return redirect(url_for('itemlisting'))

if __name__ == '__main__':
    app.run(debug = True)