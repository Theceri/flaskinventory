from flask import Flask, render_template, request, redirect, url_for
from configs.base_config import Development, Staging, Production
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2

app = Flask(__name__)
app.config.from_object(Development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/sqlalchemy'
# db = SQLAlchemy(app)

@app.route('/', methods = ['GET', 'POST'])
def itemlisting():
    if request.method == 'GET':
        return render_template('items.html')
    else:
        item_name = request.form['item_name']
        item_quantity = request.form['item_quantity']
        item_buying_price = request.form['item_buying_price']
        item_selling_price = request.form['item_selling_price']

        print(item_name, item_quantity, item_buying_price, item_selling_price)
        
        return redirect(url_for('itemlisting'))

if __name__ == '__main__':
    app.run(debug = True)