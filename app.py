from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
# Database 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
 # Init db 
db = SQLAlchemy(app)
# Isnit ma
ma=Marshmallow(app)

# product /class Model
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    description=db.Column(db.String(200))
    price=db.Column(db.String(100))

    def __init__(self,name,description,price):
        self.name=name
        self.description=description
        self.price=price
# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields=('id','name','description','price')

#Init Schema 
product_schema=ProductSchema(strict=True)
products_schema=ProductSchema(many=True,strict=True)

# create Product  (Post)
@app.route('/add',methods=['POST'])
def add_product():
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    new_product=Product(name,description,price)  
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)
#fetch all products
@app.route('/products',methods=['GET'])
def get_products():
    all_products=Product.query.all()
    result=products_schema.dump(all_products)  
    return jsonify(result.data)
#fetch One  products
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product)   
# Update Product  (Put)
@app.route('/update/<id>',methods=['PUT'])
def update_product(id):
    product=Product.query.get(id)
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    product.name=name
    product.description=description
    product.price=price
    db.session.commit()
    return product_schema.jsonify(product)    
#Delete  products
@app.route('/delete/<id>',methods=['DELETE'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)       
#run server   
if __name__=='__main__':
    app.run(debug=True)