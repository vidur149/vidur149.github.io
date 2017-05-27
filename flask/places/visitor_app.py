from flask import Flask,request,abort,jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
auth =HTTPBasicAuth()
app =Flask(__name__)

app.config.update({
   "DEBUG": True
})

users =[
   {
       'username': 'aslam',
       'password': 'aslam',
       'age': 18,
       'city': 'delhi sarita vahar',
       'bio': "hello this is Aslam and I am learning programming"
    },
   {
       'username': 'nitin',
       'password': 'nitin',
       'age': 25,
       'city': 'delhi sarita vihar',
       'bio': "hello this is Nitin and i am learning programming at navgurukul"
   },
    {
        'username': 'rahul',
        'password': 'rahul',
        'age': 25,
        'city': 'delhi sarita vihar',
        'bio': "hello this is Rahul and i am learning programming at navgurukul"
    }

]

places =[
   {
       'username': 'aslam',
       'placename': 'delhi',
       'addedOn': datetime.now(),
       'details': 'a very crowded city but with nice street food',
       'likes': 500,
       'id': 1
    },
   {
       'username': 'nitin',
       'placename': 'sarita vihar',
       'addedtime': datetime.now(),
       'details': 'homely place with lots and lots of green cover',
       'likes': 400,
       'id': 2
   },
   {
       'username': 'rahul',
       'placename': 'us',
       'addedOn': datetime.now(),
       'details': 'Woow',
       'likes': 300,
       'id': 3
   }

]

comments =[
   {
       'id': 1,
       'username': 'aslam',
       'text': "wow this course is awesome",
       'addedOn': datetime.now()
   },
   {
       'id': 3,
       'username': 'rahul',
       'text': "wow this course is awesome",
       'addedOn': datetime.now()
   },
   {
       'id': 2,
       'username': 'nitin',
       'text': "wow this course is awesome",
       'addedOn': datetime.now()
   }

]

@auth.get_password
def get_password(username):
    user =[user for user in users if username == user['username']]
    if len(user) == 0:
        abort(400)
    return user[0]['password']

@auth.error_handler
def unauthorzed():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)

@app.route('/places', methods=['GET'])
@auth.login_required
def get_places():
    place =[place for place in places if auth.username() == place['username']]
    return jsonify({'places': place})

@app.route('/search', methods=['GET'])
@auth.login_required
def search_place():
    search = request.args.get('search')
    Place = [for place in places if place['placename'] == search]
    if len(Place) == 0:
        return jsonify({'result': 'place not found'})
    return jsonify({'place': Place})

@app.route('/place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_place(place_id):
    place =[place for place in places if auth.username() == place['username']]
    if len(place) != 0:
        Place =[Place for Place in place if place_id == Place['id']]
        if len(Place)!= 0:
            return jsonify({'place': Place})
        else:
            return jsonify({'result': 'palce not found'})
    else:
        return jsonify({'result': 'user not found'})

@app.route('/user', methods=['GET'])
@auth.login_required
def get_user_details():
   user =[user for user in users if auth.username() == user['username']]
   return jsonify({'user': user})

@app.route('/signup', methods=['POST'])
@auth.login_required
def creat_user():
   if not request.json or not 'username' in request.json or not 'password' in request.json or not 'age' in request.json or not 'city' in request.json or not 'bio' in request.json:
       abort(400)
   new_user={
       'username': request.json['username'],
       'password': request.json['password'],
       'age': request.json['age'],
       'city': request.json['city'],
       'bio': request.json['bio']
   }
   users.append(new_user)
   return jsonify({'user':users}), 201

@app.route('/add/place', methods=['POST'])
@auth.login_required
def add_place():
   if not request.json or not 'placename' in request.json or not 'details' in request.json:
       abort(400)
   new_place ={
       'place': request.json['placename'],
       'addedOn': datetime.now(),
       'details': request.json['details'],
       'likes': 0,
       'id': places[-1]['id'] +1,
       'username': auth.username()
   }
   places.append(new_place)
   return jsonify({'places': places}), 201


@app.route('/change_details/change/<int:details_id>', methods=['PUT'])
@auth.login_required
def update_details(details_id):
    detail = [detail for detail in places if detail['id'] == details_id]
    if len(detail) == 0:
         abort(404)
    if not request.json:
         abort(400)
    if 'details' in request.json and type(request.json['details']) is not unicode:
         abort(400)
    detail[0]['details'] = request.json.get('details', detail[0]['details'])
    return jsonify({'detail': detail[0]})

@app.route('/user/add_comment/<int:comment_id>', methods=['POST'])
@auth.login_required
def add_comment(comment_id):
   if not request.json and not 'text' in request.json:
       abort(400)
   comment =[comment for comment in comments if comment_id ==comment['id']]
   user_comment1 =[user_comment1 for user_comment1 in comment if auth.username() ==user_comment1['username']]
   user_comment ={
       'text': request.json['text'],
       'username': auth.username(),
       'addedOn': time.strftime("%d/%m/%Y")
   }
   comments.append(user_comment)
   return jsonify({'comment': comment})

if __name__ == "__main__":
    app.run()