from flask import Flask, jsonify, abort, request, make_response, url_for
import json

app = Flask(__name__, static_url_path = "")

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route("/")
@app.route("/api", methods = ['GET', 'POST'])
def booksFunction():
   if request.method == 'GET':
       return get_tasks()
   elif request.method == 'POST':
       print(request.get_json())
       id = request.get_json()['id']
       title = request.get_json()['title']
       description = request.get_json()['description']
       return create_task(id,title,description)

@app.route("/api/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def bookFunctionId(id):
   if request.method == 'GET':
       return get_task(id) 
   elif request.method == 'POST':
       id = request.get_json()['id']
       title = request.get_json()['title']
       description = request.get_json()['description']
       return create_task(id,title,description)
    
def get_tasks():
   return jsonify([t for t in tasks])
   
def get_task(task_id):
   return jsonify([task for task in tasks if task_id == task['id']])

def create_task(id,title,description):
   task = {}
   task['id']= id
   task['title'] = title
   task['description'] = description
   task['done'] = False
   tasks.append(task)
   return jsonify("Task Added: {}".format(task))

if __name__ == '__main__':
    app.run(debug = True)
