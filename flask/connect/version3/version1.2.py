from flask import Flask, request, jsonify, abort, make_response, send_from_directory, url_for
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import os
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

users = [
    {
        'id': 0,
        'username': 'vidur',
        'password': 'vidur',
        'dp': ''
    },
    {
        'id': 1,
        'username': 'navgurukul',
        'password': 'ng',
        'dp': ''
    },
     {
        'id': 2,
        'username': 'rahul',
        'password': 'rahul',
        'dp': ''
    },
    {
        'id': 3,
        'username': 'dhannu',
        'password': 'dhannu',
        'dp': ''
    }
]

posts = [
    {
        'id': 1,
        'username': 'vidur',  
        'datetime': datetime(2017, 5, 22, 15, 47, 57, 590729), 
        'content': 'iss api se hum ng ke logon se connect kar sakte hai',
        'total_likes': 10,
        'comments': [
            {
                'id': 1,
                'post_id': 1,
                'username': 'vidur',
                'content': 'bhot badia',
                'datetime': datetime(2017, 5, 22, 16, 47, 57, 590729),
                'comments': [
                    {
                        'id': 31,
                        'username': 'vidur',
                        'content': 'bhot badia',
                        'datetime': datetime(2017, 5, 22, 16, 47, 57, 590729),
                    }
                ]
            }        
        ]
    }
]


messages = [
    {
        'id': 1,
        'sender': 'vidur',
        'receiver': 'navgurukul',
        'content': 'Hey! Wassup?',
        'datetime': datetime(2017, 5, 22, 17, 48, 57, 590729),
    },
    {
        'id': 2,
        'sender': 'navgurukul',
        'receiver': 'vidur',
        'content': 'Learning flask?',
        'datetime': datetime(2017, 5, 22, 17, 58, 57, 590729),
    },
    {
        'id': 3,
        'sender': 'rahul',
        'receiver': 'vidur',
        'content': 'Hey??',
        'datetime': datetime(2017, 5, 22, 19, 58, 57, 590729),
    },
    {
        'id': 4,
        'sender': 'navgurukul',
        'receiver': 'vidur',
        'content': 'Yes! Learning Flask',
        'datetime': datetime(2017, 5, 22, 20, 58, 57, 590729),
    },
    {
        'id': 5,
        'sender': 'rahul',
        'receiver': 'vidur',
        'content': 'there??',
        'datetime': datetime(2017, 5, 22, 21, 58, 57, 590729),
    }
]


@auth.get_password
def get_password(username):
    user = [user for user in users if user['username'] == username]
    if len(user) != 0:
        return user[0]['password']
    return None


@auth.error_handler
def unauthorized():
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/signup', methods=['POST'])
def signup():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    user = [user for user in users if user['username'] == request.json['username']]
    if len(user) == 0:    
        if len(users) != 0:
            id = users[-1]['id'] + 1
        else:
            id = 0
        new_user = {
            'id': id,
            'username': request.json['username'],
            'password': request.json['password'],
            'dp': ''
        }
        users.append(new_user)
        return jsonify({'result': True}), 201
    else:
        return jsonify({'result': 'username already exsists'}), 400

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    user = [user for user in users if user['username'] == request.json['username']]
    if len(user) != 0 and user[0]['password'] == request.json['password']:    
        return jsonify({'result': True})
    else:
        return jsonify({'result': 'username or password is incorrect'}), 401

@app.route('/posts', methods=['POST'])
@auth.login_required
def newPost():
    username = auth.username()
    if not request.json or 'content' not in request.json:
        abort(400)
    if len(posts) != 0:
        id = posts[-1]['id'] + 1
    else:
        id = 0
    new_post = {
        'id': id,
        'username': username,
        'content': request.json['content'],
        'datetime': datetime.now(),
        'comments': [],
        'total_likes': 0
    }
    posts.append(new_post)
    return jsonify({'post': new_post}), 201

@app.route('/allposts', methods=['GET'])
@auth.login_required
def get_all_posts():
    return jsonify({'posts': posts})

@app.route('/posts', methods=['GET'])
@auth.login_required
def get_posts():
    username = auth.username()
    Posts = [post for post in posts if post['username'] == username]
    if len(Posts) != 0:
        return jsonify({'posts': Posts})
    else:
        abort(404)

@app.route('/posts/<int:postid>/comment', methods=['POST'])
@auth.login_required
def new_comment(postid):
    username = auth.username()
    post = [post for post in posts if post['id'] == postid]
    if len(post) != 0:
        if not request.json or 'content' not in request.json:
            abort(400)
        if  len(post[0]['comments']) !=0:
            id = post[0]['comments'][-1]['id'] + 1
        else:
            id = 0
        new_comment = {
            'id': id,
            'username': username,
            'content': request.json['content'],
            'datetime': datetime.now(),
            'comments': []
        }
        post[0]['comments'].append(new_comment)
        return jsonify({'comment': new_comment}), 200
    else:
        abort(400)


@app.route('/posts/<int:postid>/like', methods=['POST'])
@auth.login_required
def new_like(postid):
    for post in posts:
        if post['id'] == postid:
            post['total_likes'] = post['total_likes'] + 1
            return jsonify({'likes': post['total_likes']})

@app.route('/posts/<int:postid>/comment/<int:commentid>', methods=['POST'])
@auth.login_required
def new_nested_comment(commentid, postid):
    username = auth.username()
    post = [post for post in posts if post['id'] == postid]
    if len(post) != 0:
        comment = [comment for comment in post[0]['comments'] if comment['id'] == commentid]
        if len(comment) != 0:
            if not request.json or 'content' not in request.json:
                abort(400)
            if len(comment[0]['comments']) != 0:
                id = comment[0]['comments'][-1]['id'] + 1
            else:
                id = 0
            new_comment = {
                'id': id,
                'username': username,
                'content': request.json['content'],
                'datetime': datetime.now(),
            }
            comment[0]['comments'].append(new_comment)
            return jsonify({'comment': new_comment}), 200
    
    abort(400)

def allowed_file(filename):
    return filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user/upload/profilepicture', methods=['POST'])
@auth.login_required
def upload_dp():
    print request.files
    if 'file' not in request.files:
        print "heyyy"
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(404)
    username = auth.username()
    user = [user for user in users if user['username'] == username]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user[0]['dp'] = url_for('uploaded_file', filename=filename)
        return jsonify({'result': True}), 201
    else:
        return jsonify({'result': 'file format not supported'}), 400            

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)    
    abort(404)

@app.route('/messages/<string:receiver>', methods=['POST'])
@auth.login_required
def new_message(receiver):
    if not request.json or 'content' not in request.json:
        abort(400)
    sender = auth.username()
    Receiver = [user for user in users if user['username'] == receiver]
    if len(Receiver) != 0:
        if len(messages) == 0:
            id = 0
        else:
            id = messages[-1]['id'] + 1
        
        new_message = {
            'id': id,
            'sender': sender,
            'receiver': receiver,
            'content': request.json['content'],
            'datetime': datetime.now()
        }
        messages.append(new_message)
        return jsonify({'message': new_message}), 201
    else:
        abort(400)

@app.route('/messages/<string:receiver>', methods=['GET'])
@auth.login_required
def get_messages(receiver):
    sender = auth.username()
    f = False
    for user in users:
        if user['username'] == receiver:
            f = True
            break

    if f:
        Messages = [message for message in messages if ( message['sender'] == sender and message['receiver'] == receiver) or (message['sender'] == receiver and message['receiver'] == sender)]
        return jsonify({'messages': Messages})
    else:
        abort(400)

@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    username = auth.username()
    Users = {
        'users': []
    }
    for user in users:
        if user['username'] != username:
            Users['users'].append(user['username'])
    return jsonify(Users)    
# @app.route('/messages', methods=['GET'])
# @auth.login_required
# def get_people():
#     sender = auth.username()
#     chats = {
#         'people': []
#     }

#     for message in messages:
#         print message
#         if message['sender'] == sender:
#             if message['receiver'] not in chats['people']:
#                 chats['people'].append(message['receiver'])
#         if message['receiver'] == sender:
#             if message['sender'] not in chats['people']:            
#                 chats['people'].append(message['sender'])        
#     if sender in chats['people']:
#         chats['people'].remove(sender)
#     return jsonify(chats)
    
if __name__ == '__main__':
    app.run(debug=True)