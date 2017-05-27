#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import time

# auth ek application h jo authotication ke sare kam karti h
auth = HTTPBasicAuth()
# isse flash ki application ko run kart h
app = Flask(__name__)
# isse hame terminal me bar bar code chalne ki jarurt ni padti wo khud update ho jata hi
app.config.update({'DEBUG': True})

users = [{
    'username': 'rahul',
    'password': 'rahul',
    'bio': 'leranig flask',
    'age': 20,
    'city': 'delhi',
}, {
    'username': 'shivam',
    'password': 'shivam',
    'bio': 'best codder of navgurukul',
    'age': 33,
    'city': 'mubai',
}]

places = [{
    'placeName': 'taj mahal',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'taj mahal is in agra',
    'username': 'rahul',
    'likes': 10,
    'id': 1,
}, {
    'placeName': 'lal kila',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'this is red in color',
    'username': 'shivam',
    'likes': 15,
    'id': 1,
}, {
    'placeName': 'lotous temple',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'it shape is like lotus',
    'username': 'rahul',
    'likes': 16,
    'id': 2,
}, {
    'placeName': '5 sense',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'this is the love point',
    'username': 'shivam',
    'likes': 14,
    'id': 2,
}]

comments = [{
    'id': 1,
    'username': 'rahul',
    'text': 'this is not a good place to visit',
    'added_on': time.strftime('%d/%m/%Y'),
}, {
    'id': 2,
    'username': 'shivam',
    'text': 'this is not family place',
    'added_on': time.strftime('%d/%m/%Y'),
}]

# auth.get._password se user name or password check karte h isme password return karne se password khud change hota h
@auth.get_password
def get_password(username):
    # isse hum users me loop chala rahe h or check kar rahe h ki username perameter username jo hamri users ki array me h uske ke equal h ya ni
    # or yeh ek loop chalne ka tarika h jisme hum user ke under usernam ki value parameter user se match kar ke dekh rahe h ki kya wo equal h ya ni
    new_user = [user for user in users if username == user['username']]
    # isme agaer new_user ki lenth 0 hogi to error show kar do
    if len(new_user) == 0:
        abort(400)
    #  ye new_user dictionay ka password return kar rahe h
    return new_user[0]['password']


# isme agar user name or password match nhi karga to error show kar dega
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)

# isme particular user ki detail le rahe h get se
@app.route('/user/detail', methods=['GET'])
@auth.login_required
def current_user():
    # isme auth.username apne under user ka nam store kar ke check kar raha h ki jo user ne name dala h wo user ke konse username se match ho raha h
    current_user_detail = [user for user in users if auth.username() == user['username']]
    # isme jo data hota h wo json form me return kar deta h
    return jsonify({'user': current_user_detail})

# yaha par particular word search kar rahe h
@app.route('/place', methods=['GET'])
# yaha user ko username or password dalna padega jo list me h tabi wo places get kar paega or yeh get password se link hai
@auth.login_required
def search_place():
    # isse hum url me ?search dal kar place ka nam dal kar search karege. isse hume url me dal kar likh sakte h
    # request.arg.get se hum url me kuch input kar ke check karte h (isme hum url apne user me lete h)
    search =request.args.get('search')
    new_list = []
    # is loop me hum check kar rahe h ki jo user ne url me nam dal h wo places dictionary ki arrary me h ya ni agar h to use new_list me append kar do
    for place in places:
        if search in place['placeName']:
            new_list.append(place)
    # agar search ki value kisi v placeName se match ni ho rahi h ya usme kuch nhi h to error return kar do
    if len(new_list) == 0:
            new_list.append({'error': ' sorry, your search is not found'})
    return jsonify({'place': new_list}),201

# isme hame current user ke sare places me se id ke hisab se ek place ki value return kar raha h or wo id hum url se dalte h
@app.route('/get/user/user_current_place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_place(place_id):
    # yaha hum particular user ke sare places nikal rahe h auth.username() isme check kar rahe h ki kya username isme h ya ni agar h to use add kar lo
    place = [place for place in places if auth.username() == place['username']]
    # yaha hum user ke sare place ko check kar rahe h jiss place me upper wali id se match karegi wo rturn karega or jo upper place add hue the unme ye id same h ya ni ye check kar raha h
    one_place = [one_place for one_place in place if place_id == one_place['id']]
    return (jsonify({'place': one_place}), 201)

# isme particuler place ki detail nikal rahe h
@app.route('/get/user/user_comment/<int:comment_id>', methods = ['GET'])
@auth.login_required
def comment_from_id(comment_id):
    # isme place ki id ke hisab se uski sari comment lenge or isme comment_id se check kar rahe h ki comment_id place wali id ke ander h ya ni
    place_detail = [place_detail for place_detail in comments if comment_id ==place_detail['id']]
    return jsonify({'comment': place_detail}), 201

# isme hum user add kar rahe h
@app.route('/post/user/add_user', methods=['POST'])
@auth.login_required
def signup():
    # isme agar jo data h wo json form me nhi hua or username reqest.json me nhi hua to wo abort show kar dega
    if not request.json or not 'username' in request.json:
        abort(400)
    #  isme hum user ki array me user add kar rahe h
    add_user = {
        # isme hame jo jo add karna h wo hum kar rahe h
        'username': request.json['username'],
        'password': request.json['password'],
        'bio': request.json['bio'],
        'age': request.json['age'],
        'city': request.json['city'],
    }
    users.append(add_user)
    return (jsonify({'users': add_user}), 201)

# isme hum new user add kar rahe h
@app.route('/post/place/add_place', methods=['POST'])
@auth.login_required
def add_place():
    # agar
    if not request.json or not 'placeName' in request.json:
        abort(400)
    #isme jo hame user ki array me add karwna h wo likha hua h
    add_place = {
        # hame usme jo chij add karwani h wo likhni h ki usme kya kya add kar sakte h
        'placeName': request.json['placeName'],
        # time.strftime('%d/%m/%y') isse hum jis bhi date ko usme add karege wo apne ap usme wo date kar lega
        'added_on': time.strftime('%d/%m/%Y'),
        'detail': request.json['detail'],
        # auth.usrname() me jo name add tha isme wo return kar dega
        'username': auth.username(),
        # hum jab v add karege usme apne ap 1 like bad jaega
        'likes': places[-1]['likes'] + 1,
        # hum jab bhi add kaege id me ek plus ho jaega
        'id': places[-1]['id'] + 1,
    }
    # jo bhi humne uper likh h wo add places wali array me ho jae
    places.append(add_place)
    return (jsonify({'places': add_place}), 201)

# yaha humne particular user ki ek particular place par comment post kiya h
@app.route('/post/user/add_comment/<int:comment_id>', methods = ['POST'])
@auth.login_required
def add_comment(comment_id):
    # agar isme request.json me h ya ni aur isme hume text append karna h wo bhi hona chahiye agar esa nhi hua to wo abort return kar dega
    if not request.json and not 'text' in request.json:
        abort(400)
    # yaha hum ek id ke sare comment karwa rahe h matlb ek place ke sare comments return karwa rahe h

    places_comments = [comment for comment in comments if comment_id == comment['id']]

    # isse hum place ke sare comment me se ek particular user ke sare comment return karwa rahe h
    # current_user_comment =[current_user_comment for current_user_comment in comment if auth.username() == current_user_comment['username']]

    places_comments = {
        'text': request.json['text'],
        'username': auth.username(),
        'added_on': time.strftime('%d/%m/%Y'),
        'id': comment['id']
    }

    comments.append(places_comments)
    return jsonify({'comment': comments},{'all': comments})

# yaha hum id se place ki detail value ko update karege
@app.route('/put/user/update_place/<int:place_id>', methods = ['PUT'])
@auth.login_required
def update_place(place_id):
    # isme hum current/particular user ke sare places ko le rahe h or isse ye dekh rahe h ki user name places wali array ke wo user name h ya ni agar h to agge chal kar uski id check karo
    update_place_value = [update_place_value for update_place_value in places if auth.username() == update_place_value['username']]
    # yaha hum particular place ko uski id se update karege isme yehe dekhege ki jo place_id user ne dali h wo place wali id ke equal h ya ni
    place_update = [place_update for place_update in update_place_value if place_id == place_update['id']]
    if len(place_update) == 0:
        abort(400)
    if not request.json:
        abort(400)
    # yaha detail requst.json me hi honi chahiye or request.json['detail'] ye unicode me nhi honi chahiye matlb wo change ho sake ese honi chahiye
    # jo request jati or ati h use request.json json me convert kar deta hai
    if 'detail' in request.json and type(request.json['detail']) is not unicode:
        abort(400)
    # sath me .get lagne se agar use deatail nhi milti to wo khali string return kar deta h
    place_update[0]['detail'] = request.json.get('detail', place_update[0]['detail'])
    return jsonify({'update_place': place_update[0]})

if __name__ == '__main__':
    app.run()