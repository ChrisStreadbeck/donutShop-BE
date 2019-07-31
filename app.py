from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Donut(db.Model):
    __tablename__ = "donuts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(255))
    image = db.Column(db.String(500))
    price = db.Column(db.Integer)
    
    def __init__(self, title, text, image, price):
        self.title = title
        self.text = text
        self.image = image
        self.price = price

class DonutSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "text", "image", "price")

donut_schema = DonutSchema()
donuts_schema = DonutSchema(many=True)

@app.route("/")
def greeting():
    return "<h1>Donut API</h1>"










if __name__ == "__main__":
    app.debug = True
    app.run()