import time
from flask import Flask, jsonify, request, abort, make_response, Response
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId   

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
app.config["MONGO_DBNAME"] = "ecom_db"
mongo = PyMongo(app, config_prefix='MONGO')
app.config.update({
    "DEBUG": True
})

users =[
    {   
        'id': 0,
        'username': 'shivam', 
        'password': 'jaan', 
        'age': 26, 
        'city': 'sarita vihar', 
        'bio': "hi i am shivam and i am learning programming at navgurukul"
    },
    {
        'id': 1,
        'username': 'jaan',
        'password': 'shivam',
        'age': 22,
        'city': 'gurgaon',
        'bio': "hi i am jann and i am jaan of my shivam"
    }
]

places = [
    {
        'id': 0,
        'username': 'shivam',
        'placeName': 'Mandaula',
        'addedOn': time.strftime("%d/%m/%Y"),
        'details': 'this is an awesome place for everyone',
        'likes': 200
    },
    {
        'id': 1,        
        'username': 'jaan',
        'placeName': 'Saket',
        'addedOn': time.strftime("%d/%m/%Y"),
        'details': 'this is an awesome place for every couple',
        'likes': 2300
    },
    {
        'id': 2,        
        'username': 'shivam',
        'placeName': 'Red Fort',
        'addedOn': time.strftime("%d/%m/%Y"),
        'details': 'this is place of ancient kings',
        'likes': 210
    },
    {   
        'id': 3,
        'username': 'jaan',
        'placeName': 'Garden of Five Senses',
        'addedOn': time.strftime("%d/%m/%Y"),
        'details': 'this is the best place for every couple',
        'likes': 2300
    }
]

comments =[
    {
        'username': 'jaan',
        'placeId': 2,
        'content': " It was the main residence of the emperors of the Mughal dynasty for nearly 200 years",
        'addedOn': time.strftime("%d/%m/%Y")
    },
    {
        'username': 'shivam',
        'placeId': 3,
        'content': "The Garden of Five Senses is a park spread over 20 acres",
        'addedOn': time.strftime("%d/%m/%Y")
    },
    {
        'username': 'shivam',
        'placeId': 1,
        'content': "The pace of development in saket is high these days.",
        'addedOn': time.strftime("%d/%m/%Y")
    }
]

@auth.get_password
def get_password(username):
    user = [user for user in users if username == user['username']]
    if len(user) == 0:
        abort(400)
    return user[0]['password']

@auth.error_handler
def unauthorzed():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)


@app.route('/places', methods=['GET'])
@auth.login_required
def get_place_form_search():
    search = request.args.get('search')
    if search:
        new_list = []
        for place in places:
            if search in place['placeName']:
                new_list.append(place)
        if len(new_list) == 0:
            new_list.append({'typeError':'sorry, your search word does not exist in our server'})
        return jsonify({'places': new_list})
    else:
        abort(400)

@app.route('/place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_user_particular_place(place_id):
    place = [place for place in places if auth.username() == place['username'] and place['id'] == place_id]
    if len(place) == 0:
        abort(404)
    return jsonify({'place': place})    

@app.route('/user', methods=['GET'])
@auth.login_required
def get_current_user_details():
    user = [user for user in users if auth.username() == user['username']]
    return jsonify({'user': user})

@app.route('/place/<int:place_id>/update', methods=['PUT'])
@auth.login_required
def update_place_from_id(place_id):
    place = [place for place in places if auth.username() == place['username'] and place['id'] == place_id]
    if len(place) == 0:
       abort(404)
    if not request.json or 'details' not in request.json and type(request.json['details']) is not unicode or 'placeName' not in request.json and type(request.json['placeName']) is not unicode: 
       abort(400)
    place[0]['details'] = request.json.get('details', place[0]['details'])
    place[0]['placeName'] = request.json.get('placeName', place[0]['placeName'])
    place[0]['username'] = auth.username()    
    return jsonify({'update_place': place[0]})

@app.route('/place/add', methods=['POST'])
@auth.login_required
def new_place():
    if not request.json and not 'placeName' in request.json and not 'details' in request.json:
        abort(400)
    place ={
        'placeName': request.json['placeName'],
        'addedOne': time.strftime("%d/%m/%Y"),
        'details': request.json['details'],
        'likes': 0,
        'id': places[-1]['id'] +1,
        'username': auth.username()
    }
    places.append(place)
    return jsonify({'places': places}), 201

@app.route('/signup', methods=['POST'])
def creat_user():
    if not request.json:
        abort(400)
    new_user = {
        'username': request.json['username'],
        'password': request.json['password'],
        'age': request.json['age'],
        'city': request.json['city'],
        'bio': request.json['bio']
    }
    users.append(new_user)
    return jsonify({'user': users}), 201

@app.route('/place/<int:place_id>/comment', methods=['POST', 'GET'])
@auth.login_required
def add_comment(place_id):
    if request.method == 'GET':
        Comments = [comment for comment in comments if comment['placeId'] == place_id]
        if len(Comments) == 0:
            abort(404)
        return jsonify({"comments": Comments})
    elif request.method == 'POST':
        if not request.json and not 'content' in request.json:
            abort(400)
        new_comment ={
            'content': request.json['content'],
            'username': auth.username(),
            'placeId': place_id,
            'addedOn': time.strftime("%d/%m/%Y")
        }
        comments.append(new_comment)
        return jsonify({'comment': comments})

@app.route('/place/<int:place_id>/like', methods=['POST'])
@auth.login_required
def like_place(place_id):
    place = [place for place in places if place['id'] == place_id]
    if len(place) == 0:
        abort(404)
    place[0]['likes'] = place[0]['likes'] + 1    
    return jsonify({"likes": place[0]['likes']})

if __name__ =="__main__":
    app.run()