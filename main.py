from flask import Flask, render_template, request, redirect, url_for
from configs.base_config import Development, Staging, Production
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2

app = Flask(__name__)
app.config.from_object(Development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/sqlalchemy'
# db = SQLAlchemy(app)

@app.route('/', methods = ['GET', 'POST'])
def helloworld():
    return "Hello world"