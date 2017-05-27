import time

from flask import Flask,request,abort,jsonify, make_response
from flask_httpauth import HTTPBasicAuth

# here i made "auth" as an application which would for all work related to authentication
auth =HTTPBasicAuth()
# isse flask ki application ka intialization hota hia
app =Flask(__name__)
# this would help us for time to time update our code in terminal that means we dont need to run server again automaticaly it would be updated
app.config.update({
    "DEBUG": True
})

users =[
    {'username': 'shivam', 'password': 'jaan', 'age': 26, 'city': 'sarita vihar', 'bio': "hi i am shivam and i am learning programming at navgurukul"},
    {'username': 'jaan', 'password': 'shivam', 'age': 22, 'city': 'gurgaon', 'bio': "hi i am jann and i am jaan of my shivam"}
]

places =[
    {'username': 'shivam','placeName': 'mandaula', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for everyone', 'likes': 200, 'id': 1},
    {'username': 'jaan','placeName': 'saket', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for every couple', 'likes': 2300, 'id': 2},
    {'username': 'shivam','placeName': 'lal kila', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is place for incient kings', 'likes': 210, 'id': 3},
    {'username': 'jaan','placeName': 'five sence', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for every couple', 'likes': 2300, 'id': 2}
]

comments =[
    {'username': 'jaan','id': 2, 'text': "i love this place and i am owner of the place", 'addedOn': time.strftime("%d/%m/%Y")},
    {'username': 'shivam','id': 3, 'text': "this is famous place since 1990", 'addedOn': time.strftime("%d/%m/%Y")},
    {'username': 'shivam','id': 2, 'text': "kdsjfjkljsklfjsdklfj", 'addedOn': time.strftime("%d/%m/%Y")}
]


# this keyword is for check username and password that means we need authenticate from taking base from @auth.get_pasword keyword
@auth.get_password
def get_password(username):
    # in this we are trying to run loop at users array and in this array we would check the username is equal to or not user['username']
    user =[user for user in users if username ==user['username']]
    # yha humne ye check kiya hia ki agar user ki length 0 hai to error show kar do
    if len(user) == 0:
        abort(400)
    # yha humne user nam ki dictionary ka  password return kiya hia aur fir ye password check karna browser ka kam hia ki wo dala gye password se match karta hia ya ni
    return user[0]['password']


# agar username and password dono match na ho to ye error show karne k liye ye function banaya hai
@auth.error_handler
def unauthorzed():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)


# yha hum user ke search k according sari places ko dikha rhe hai
@app.route('/get/user/places', methods=['GET'])
# yha hum user se pehle login karne k liye kahenge iska matalb user ko places get karne k liye pehle user ko login karna padega
# ye upper get_password function se connect ho rha hia from @auth se
@auth.login_required
def get_place_form_search():
    # yha hum user se url mei ? ke bad search variable ki value le rhe hai
    search = request.args.get('search')
    new_list = []
    # yha hum search variable ki value ko filter kar rhe hia from all places
    for place in places:
        if search in place['placeName']:
            new_list.append(place)
    # agar search keyword ki value kisi bhi place se match ni kar rhi to ye return karna hia
    if len(new_list) == 0:
        new_list.append({'typeerror':'sorry, your search word does not exist in our server'})
    return jsonify({'user_place': new_list}), 201


# yha humne current user ki sari places mei se ek place return karai hia aur wo ek place ki id triger karne k liye humne url mei int se li hia
@app.route('/get/user/current_user_one_place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_user_particular_place(place_id):
    # yha humne ek particular user ki sari places  return karai hia
    place =[place for place in places if auth.username() == place['username']]
    # aur yha hum user ki sari place ko check kar rhe hai aur jiss place ki id upper wali place_id se match karegi wo return kiya hia
    one_place =[one_place for one_place in place if place_id == one_place['id']]
    return jsonify({'user_place': one_place}), 201


# here i am trying to get the details of one place
@app.route('/get/user/comment_from_id/<int:comment_id>', methods=['GET'])
@auth.login_required
def get_details_place_from_id(comment_id):
    # here i will get all comments dictionary who have same id equal to comment_id which i will get from user at url or endpoint
    place_details =[one_comment for one_comment in comments if comment_id ==one_comment['id']]
    return jsonify({'user_place': place_details}), 201


# here i will get details of particular user for filling their profile details on frontend page
@app.route('/get/user/current_user_details', methods=['GET'])
@auth.login_required
def get_current_user_details():
    user =[user for user in users if auth.username() == user['username']]
    return jsonify({'user_place': user}), 201



# here i am trying to update the details of particular place it would be happend accroding to id
@app.route('/put/user/update_place/<int:place_id>', methods=['PUT'])
@auth.login_required
def update_place_from_id(place_id):
    # first of all we are trying to get all places of particular user
    all_user_place =[all_user_place for all_user_place in places if auth.username() ==all_user_place['username']]
    # now i have all place of that user and now i need to find out which place should be update for this i will check place_id is equal to or not to place['id']
    id_place =[id_place for id_place in all_user_place if place_id ==id_place['id']]
    # if the user input id in url does not match to any place then 404 would be return
    if len(id_place) == 0:
       abort(404)
    # if the request.json does not exist then 400 would be return
    if not request.json:
       abort(400)
    # 'details'  must be in request.json and request.json['details'] must not be unicode  means it could be change
    if 'details' in request.json and type(request.json['details']) is not unicode:
       abort(400)
    if 'likes' in request.json and type(request.json['likes']) is not unicode:
       abort(400)
    # yha hum place ki details me kuch edit karte hai aur sath hi sath likes bhi badhate hai
    # yaha par request.json karne par details add hote hai jab hum json se data bhejte hai aur
    # sath m .get lagane par agar use details nahi milti to wo khali string return kar dete hai
    id_place[0]['details'] = request.json.get('details', id_place[0]['details'])
    # yha hum particular place ke likes update ki hia agar wo update ni ho to wo  as is it return kar deta hia
    id_place[0]['likes'] =request.json.get('likes', id_place[0]['likes'])
    return jsonify({'update_place': id_place[0]})



# here i am trying to get  creat a new user means signup
@app.route('/post/user/signup', methods=['POST'])
@auth.login_required
def creat_user():
    # if the request.json does not exist and in it 'user' must be there
    if not request.json and not 'user' in request.json:
        abort(400)
    # for posting key values we need to write request.json with that key
    user={
        'username': request.json['username'],
        'password': request.json['password'],
        'age': request.json['age'],
        'city': request.json['city'],
        'bio': request.json['bio']
    }
    users.append(user)
    return jsonify({'user':users}), 201



# yha hum new  place dal rhe hai
@app.route('/post/user/addplace', methods=['POST'])
@auth.login_required
def new_place():
    # if the request.json does not exist and in it 'placeName' must be there
    if not request.json and not 'placeName' in request.json:
        abort(400)
    # yha hum place  ke  har element k content  ko dalne k liye use  element  ke aage  request.json likh  rhhe hia
    place ={
        'placeName': request.json['placeName'],
        'addedOne': time.strftime("%d/%m/%Y"),
        'details': request.json['details'],
        'likes': request.json['likes'],
        'id': places[-1]['id'] +1,
        'username': auth.username()
    }
    places.append(place)
    return jsonify({'places': places}), 201



# yha humne particular user ki ek  particular place par comment post  ki hia
@app.route('/post/user/add_comment/<int:comment_id>', methods=['POST'])
@auth.login_required
def add_comment(comment_id):
    # if the request.json does not exist and in it 'text' must be there means jo likh kar append karna hia wo request mei hona chahiye
    if not request.json and not 'text' in request.json:
        abort(400)
    # yha  hum ek id ki jitni bhi comments  hia wo return karwa rhe hia means ek place ke sare comments return kar rha hai

    all_comments_place =[comment for comment in comments if comment_id ==comment['id']]

    # aur fir yha hum ek place k sare comment mei se particular user ki comment nikal rhe hia
    # particular_user_comment =[particular_user_comment for particular_user_comment in comment if auth.username() ==particular_user_comment['username']]
    comment ={
        'text': request.json['text'],
        'username': auth.username(),
        'id': comment['id'],
        'addedOn': time.strftime("%d/%m/%Y")
    }
    comments.append(comment)
    # here  we are returning all comments because there one comment of a place has to added that's' why we  need to check the comment would or not append
    return jsonify({'comment': comments})


if __name__ =="__main__":
    app.run()