from flask import Flask, request, jsonify
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
from models import db, init_db, Task

app = Flask(__name__)
CORS(app)

init_db()
db.connect()
db.create_tables([Task], safe=True)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = [model_to_dict(t) for t in Task.select()]
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task.create(title=data['title'], done=data.get('done', False))
    return jsonify(model_to_dict(task)), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.get_or_none(Task.id == task_id)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.done = data.get('done', task.done)
        task.save()
        return jsonify(model_to_dict(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.get_or_none(Task.id == task_id)
    if task:
        task.delete_instance()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)