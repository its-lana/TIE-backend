from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class TableRepo:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.table_extraction_database
        self.tables = self.db.table_collection

    def get_id(self, table_id):
        table_extraction_data = self.tables.find_one({"_id": ObjectId(table_id)})
        table_extraction_data = json.loads(json_util.dumps(table_extraction_data))
        table_extraction_data["_id"] = table_extraction_data["_id"]["$oid"]
        return table_extraction_data

    def get_all(self):
        cursor = self.tables.find({})
        tables_extraction_data = list(cursor)
        tables_extraction_data = json.loads(json_util.dumps(tables_extraction_data))
        for item in tables_extraction_data:
            item["_id"] = item["_id"]["$oid"]
        return tables_extraction_data

    def save(self, table_extraction_data):
        persisted_data = self.tables.insert_one(table_extraction_data)
        new_id = json.loads(json_util.dumps(persisted_data.inserted_id))
        return list(new_id.values())[0]

    def update(self, table_extraction_data):
        table_id = table_extraction_data["_id"]
        del table_extraction_data["_id"]
        result = self.tables.update_one(
            filter={"_id": ObjectId(table_id)}, update={"$set": table_extraction_data}
        )
        return result.modified_count

    def delete(self, table_id):
        result = self.tables.delete_one({"_id": ObjectId(table_id)})
        return result.deleted_count
