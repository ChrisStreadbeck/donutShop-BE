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

@app.route("/donuts", methods=["GET"])
def get_donuts():
    all_donuts = Donut.query.all()
    result = donuts_schema.dump(all_donuts)
    return jsonify(result.data)

@app.route("/add-donut", methods=["POST"])
def add_donut():
    title = request.json["title"]
    text = request.json["text"]
    image = request.json["image"]
    price = request.json["price"]

    new_donut = Donut(title, text, image, price)

    db.session.add(new_donut)
    db.session.commit()

    return jsonify("DONUT POSTED!")


@app.route("/donut/<id>", methods=["PUT"])
def update_donut(id):
    if request.content_type == "application/json":
       put_data = request.get_json()

       title = put_data.get("title")
       text = put_data.get("text")
       image = put_data.get("image")
       price = put_data.get("price")

       record = db.session.query(Donut).get(id)
       record.title = title
       record.text = text 
       record.image = image
       record.price = price 


       db.session.commit()
       return jsonify("Update Successful")
    return jsonify("Check content_type and try again")

@app.route("/donut/<id>", methods=["DELETE"])
def delete_donut(id):
    record = db.session.query(Donut).get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Record DELETED!!") 


if __name__ == "__main__":
    app.debug = True
    app.run()