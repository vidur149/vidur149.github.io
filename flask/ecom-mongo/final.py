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
app.config["MONGO_DBNAME"] = "ecom_app"
mongo = PyMongo(app, config_prefix='MONGO')

@auth.get_password
def get_password(username):
    print username
    user = mongo.db.users.find_one_or_404({'username': username})
    return (user['password'])

@auth.error_handler
def unauthorized():
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/signup', methods=['POST'])
def signup():
  if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
  if mongo.db.users.find({'username': request.json['username']}).count() == 0:
    new_user = {
      'username': request.json['username'],
      'password': request.json['password'],
    }
    mongo.db.users.insert(new_user)
    return jsonify({'result': True}), 201
  else:
    return jsonify({'result': 'user already exsists'})

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    user = mongo.db.users.find_one({'username': request.json['username']})
    if user and user['password'] == request.json['password']:
        return jsonify({'result': True})
    else:
        return jsonify({'result': 'username or password is incorrect'}), 401

@app.route('/products', methods=['GET'])
def products():
    resp = {
        'data': list(mongo.db.products.find())
    }
    return Response(dumps(resp), mimetype='application/json')

@app.route('/product/<string:p_id>', methods=['GET'])
def get_product(p_id):
    resp = {
        'data': list( mongo.db.products.find({"_id": ObjectId(p_id)}) )
    }
    return Response(dumps(resp), mimetype='application/json')

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
    product['reviews'] = reviews
    updated_product = mongo.db.products.update({"_id": ObjectId(p_id)}, product)
    return jsonify({"success": True})

@app.route('/cart', methods=['GET'])
@auth.login_required
def get_cart_details():
  username = auth.username()  
  resp = {
    'data': list(mongo.db.carts.find({"username": username}))
  }
  return Response(dumps(resp), mimetype='application/json')


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
    if product['_id'] == p_id:
      product['quantity'] = product['quantity'] + 1
      new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
      resp = {
        'cart': list(mongo.db.carts.find({"username": username}))
      }
      return Response(dumps(resp), mimetype='application/json')
    
  new_product = { '_id': str(Product['_id']), 'quantity': 1 }
  product_list.append(new_product)
  new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
  resp = {
    'cart': list(mongo.db.carts.find({"username": username}))
  }
  return Response(dumps(resp), mimetype='application/json') 

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
      if str(product['_id']) == str(ObjectId(p_id)):
          product_list.pop(i)
          new_cart = mongo.db.carts.update({"username": username},{"username": username, "products": product_list})
          resp = {
              'cart': list(mongo.db.carts.find({"username": username}))
          }
          return Response(dumps(resp), mimetype='application/json')
          break
    return jsonify({'result': 'product not in cart'})          
  else:
    return jsonify({'result': 'product list is empty'})

@app.route('/checkout', methods=['POST'])
@auth.login_required
def checkout():
    username = auth.username()
    if mongo.db.carts.find({"username": username}).count() == 0:
        return jsonify({"response": 'cart not found'})
    cart = mongo.db.carts.find_one_or_404({"username": username})
    product_list = cart['products']
    new_order = {
        "datetime": datetime.now(),
        "username": username,
        "products": product_list
    }
    mongo.db.orders.insert(new_order)
    result = mongo.db.carts.remove({"username": username})
    return Response(dumps({"data": list(mongo.db.orders.find({"username": username}))}), mimetype='application/json')

if __name__ == '__main__':
  app.run(debug=True)
