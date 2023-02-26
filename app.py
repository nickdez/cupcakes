"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
db.create_all()

@app.route("/")
def home():
    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)

@app.route("/api/cupcakes")
def list_cupcakes():
    
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():

    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(new_cupcake=new_cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    data = request.json

    flavor=data['flavor'],
    rating=data['rating'],
    size=data['size'],
    rating=data['rating'],
    image=data['image'],

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake():

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake Deleted")

