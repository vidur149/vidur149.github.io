from flask import Flask, jsonify, request, abort, make_response, Response
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId   

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
app.config["MONGO_DBNAME"] = "ecom_db"
mongo = PyMongo(app, config_prefix='MONGO')

@auth.get_password
def get_password(username):
    user = mongo.db.user.find_one_or_404({'username': username})
    return (user['password'])

@auth.error_handler
def unauthorized():
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

def post_products():
  mongo.db.products.insert([
    {
      "name": "Moto G4",
      "seller": "Motorola",
      "price": 20000,
      "category": "mobiles",
      "description": "Best budget Smartphone",
      "reviews": [],
    },
    {
      "name": "Iphone 5s",
      "seller": "Apple",
      "price": 25000,      
      "category": "mobiles",
      "description": "If you don't have an iphone you don't have an iphone",
      "reviews": [],
    },
    {
      "name": "Timex wx-900bt",
      "seller": "Timex",
      "price": 5000,      
      "category": "watches",
      "description": "Elegant.Classy.Mystical",
      "reviews": [],
    },
    {
      "name": "Badminton Racket",
      "price": 1000,      
      "seller": "Yonex",
      "category": "sports",
      "description": "The stiff racket structure is a delight to play with.",
      "reviews": [],
    }
  ])

  return jsonify({"result": True})

@app.route('/signup', methods=['POST'])
def signup():
  if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
  if mongo.db.user.find({'username': request.json['username']}).count() == 0:
    new_user = {
      'username': request.json['username'],
      'password': request.json['password'],
      'dp': ''
    }
    mongo.db.user.insert(new_user)
    return jsonify({'result': True}), 201
  else:
    return jsonify({'result': 'user already exsists'})

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    user = mongo.db.user.find_one({'username': request.json['username']})
    if user and user['password'] == request.json['password']:    
        return jsonify({'result': True})
    else:
        return jsonify({'result': 'username or password is incorrect'}), 401

@app.route('/products', methods=['GET'])
def products():
    return Response(dumps(list(mongo.db.products.find())), mimetype='application/json')

@app.route('/product/<string:p_id>', methods=['GET'])
def get_product(p_id):
    return Response(dumps(list(mongo.db.products.find({"_id": ObjectId(p_id)}))), mimetype='application/json')

@app.route('/products/<string:category>', methods=['GET'])
def products_cateory(category):
    return Response(dumps(mongo.db.products.find({"category": category})), mimetype='application/json')

@app.route('/products/review/<string:p_id>', methods=['POST'])
@auth.login_required
def post_review(p_id):
  username = auth.username()
  if not request.json or 'review' not in request.json or 'rating' not in request.json:
    abort(400)
  product = mongo.db.products.find_one_or_404({"_id": ObjectId(p_id)})
  reviews = product['reviews']
  for review in reviews:
    if review['username'] == username:
      review['review'] = request.json['review']
      review['rating'] = request.json['rating']
      review['datetime'] = datetime.now()      
      updated_product = mongo.db.products.update({"_id": ObjectId(p_id)},{ "reviews": reviews})
      return jsonify({"product": updated_product})  

  new_review = {
    "username": username,
    "review": request.json['review'],
    "rating": request.json['rating'],
    "datetime": datetime.now(),
  }
  reviews.append(new_review)
  updated_product = mongo.db.products.update({"_id": ObjectId(p_id)},{ "reviews": reviews})
  return jsonify({"product": updated_product})
  # mongo.db.products.update({"_id":ObjectId(p_id)},{"$push":{"reviews":{"username": username, "datetime": datetime.now(), "review": request.json['review'], "rating": request.json['rating']}}})  

@app.route('/cart/add/<string:p_id>', methods=['POST'])
@auth.login_required
def add_cart(p_id):
  Product = mongo.db.products.find_one_or_404({"_id": ObjectId(p_id)})
  username = auth.username()
  if mongo.db.carts.find({"username": username}).count() == 0:
    mongo.db.carts.insert({
      "username": username,
      "products": []
    })
  cart = mongo.db.carts.find_one_or_404({"username": username})
  product_list = cart['products']
  quantity = 0
  for product in product_list:
    if product['_id'] == ObjectId(p_id):
      product['quantity'] = product['quantity'] + 1
      new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
      return jsonify({"cart": new_cart})  

  new_product = Product
  new_product['quantity'] = 1
  product_list.append(new_product)
  new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
  return jsonify({"cart": new_cart})  
# comment

@app.route('/cart/remove/<string:p_id>', methods=['DELETE'])
@auth.login_required
def remove_product(p_id):
  Product = mongo.db.products.find_one_or_404({"_id": ObjectId(p_id)})
  username = auth.username()
  if mongo.db.carts.find({"username": username}).count() == 0:
    abort(404)
  cart = mongo.db.carts.find_one_or_404({"username": username})
  product_list = cart['products']
  print (product_list)
  if len(product_list) != 0:
    for i, product in enumerate(product_list):
      if product['_id'] == ObjectId(p_id):
          product_list.pop(i)
          new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
          return jsonify({"cart": new_cart})
          break          
  else:
    abort(404)

@app.route('/checkout', methods=['POST'])
@auth.login_required
def checkout():
  username = auth.username()
  if mongo.db.carts.find({"username": username}).count() == 0:
    abort(404)
  cart = mongo.db.carts.find_one_or_404({"username": username})
  product_list = cart['products']
  new_order = {
    "datetime": datetime.now(),
    "status": "pending",
    "username": username,
    "products": product_list
  }  
  mongo.db.orders.insert(new_order)
  result = mongo.db.carts.remove({"username": username})  
  return jsonify({"order": result})

if __name__ == '__main__':
  app.run(debug=True)

   # car = mongo.db.carts.find_one({"username": username, "products.['_id']": ObjectId(p_id)})
  # print car
  # if mongo.db.carts.find_one({"username": username, "products.$.['_id']": ObjectId(p_id)}):
  #   print "hey"
  #   mongo.db.carts.update({"username": username, "products.$.['_id']": ObjectId(p_id)}, {"$inc": {"products.$.qty": 1}})
    # mongo.db.carts.findAndModify({
    # "query": '{"username":username}, {"products": {"$elemMatch": {"_id": ObjectId(p_id)}}}',
    # "update": { "$inc": {"product.$.qty": 1}}
    # })
    # mongo.db.carts.update({"username":username},{"products":{"$elemMatch": { 
    # "_id": ObjectId(p_id) }product['name'], "price": product['price'], "qty": 0, "p_id": product['_id']}}})    
  # else:
  #   print "hettt"
  #   mongo.db.carts.update({"username":username},{"$push":{"products":{"name": product['name'], "price": product['price'], "qty": 1, "p_id": product['_id']}}})  
  # return jsonify({"result": True})