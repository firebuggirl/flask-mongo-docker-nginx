# os => import the environment variables
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

# load application object into the application variable
application = Flask(__name__)

# get environment variables using os.environ
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

# get the mongo object
mongo = PyMongo(application)
db = mongo.db

# create an index message / GET route
@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )


@application.route('/todo')
def todo():
    _todos = db.todo.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )


@application.route('/todo', methods=['POST'])
def createTodo():
    # get the JSON that you post to the route
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201
  # status code 201 CREATED


# run the application
# check if global variable, __name__, is the entry point to program, is "__main__"
if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)


