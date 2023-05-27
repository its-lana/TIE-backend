from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class TodoRepo:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.todo_database
        self.todos = self.db.todo_collection

    def get_id(self, todo_id):
        todo = self.todos.find_one({"_id": ObjectId(todo_id)})
        todo = json.loads(json_util.dumps(todo))
        todo["_id"] = todo["_id"]["$oid"]
        return todo

    def get_all(self):
        cursor = self.todos.find({})
        todos = list(cursor)
        todos = json.loads(json_util.dumps(todos))
        for item in todos:
            item["_id"] = item["_id"]["$oid"]
        return todos

    def save(self, todo):
        persisted_todo = self.todos.insert_one(todo)
        new_id = json.loads(json_util.dumps(persisted_todo.inserted_id))
        return list(new_id.values())[0]

    def update(self, todo):
        todo_id = todo["_id"]
        del todo["_id"]
        result = self.todos.update_one(filter={"_id": ObjectId(todo_id)}, update={"$set": todo})
        return result.modified_count

    def delete(self, todo):
        result = self.todos.delete_one({"_id": ObjectId(todo)})
        return result.deleted_count

