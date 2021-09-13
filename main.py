from flask import Flask, request
from flask_restful import Resource, Api

f = Flask(__name__)
a = Api(f)

todos = {"test1": "buy something"}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}  # get from todos: something

    def put(self, todo_id):
        todos[todo_id] = request.form["data"]
        return {todo_id: todos[todo_id]}


a.add_resource(TodoSimple, "/<string:todo_id>")


if __name__ == "__main__":
    f.run(debug=True)
