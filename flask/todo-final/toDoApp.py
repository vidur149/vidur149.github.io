from flask import Flask , jsonify , request , abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


app = Flask(__name__)
app.config.update({
    "DEBUG": True
})


users = [
    {'username': 'rahul','password': '123'},
    {'username': 'shivam','password': '456'},
    {'username': 'nitin','password': '789'}
 ]

tasks = [
    {
        'id':1,
        'title':'Learn Python',
        'description' : 'Python is important for developing unerstading of basic programming logic.',
        'done':False
    },
    {
        'id':2,
        'title':'Learn Flask',
        'description': 'We will use Flask for developing REST apis',
        'done': False
    },
    {
        'id':3,
        'title':'Learn Angular',
        'description':'Angularjs or Angular2 or Angular4 ? :P',
        'done':False
    }

]

@auth.get_password
def get_password(username):
    new_user = [user for user in users if username == user['username']]
    if len(new_user) == 0:
        abort(404)
    return new_user[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}),401)

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/signup', methods = ['POST'])
def add_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    add = {
        'username': request.json['username'],
        'password' : request.json['password']
    }
    users.append(add)
    return jsonify({"user":add}), 201

def make_public_task(task):
    print task
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/taskz', methods=['GET'])
@auth.login_required
def get_taskz():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks' : tasks})

@app.route('/tasks', methods = ['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id' : tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    # isme task naam ka variable mei hume ek loop chalaya aur uske andar ek if condition lagayi jo kehti hai
    # for task in tasks:
        # if task[id] == task_id:
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run()