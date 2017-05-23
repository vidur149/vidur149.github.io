from flask import Flask, request, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

users = [{
    'id': 0,
    'username': 'vidur',
    'password': 'vidur'
}]

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
                'username': 'vidur',
                'content': 'bhot badia',
                'datetime': datetime(2017, 5, 22, 16, 47, 57, 590729),
            }
        ]
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
            'password': request.json['password']
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
        'total_likes': 0,
        'comments': []
    }
    posts.append(new_post)
    return jsonify({'post': new_post}), 200

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
        }
        post[0]['comments'].append(new_comment)
        return jsonify({'comment': new_comment}), 200
    else:
        abort(400)

@app.route('/posts/<int:postid>/comment', methods=['GET'])
@auth.login_required
def get_comments(postid):
    post = [post for post in posts if post['id'] == postid]    
    if len(post) != 0:
        return jsonify({'comments': post[0]['comments']})
    else:
        abort(404)

@app.route('/posts/<int:postid>/like', methods=['POST'])
@auth.login_required
def new_like(postid):
    for post in posts:
        if post['id'] == postid:
            post['total_likes'] = post['total_likes'] + 1
            return jsonify({'likes': post['total_likes']})
    
    abort(404)

@app.route('/posts', methods=['GET'])
@auth.login_required
def get_posts():
    return jsonify({'posts': posts})


if __name__ == '__main__':
    app.run(debug=True)