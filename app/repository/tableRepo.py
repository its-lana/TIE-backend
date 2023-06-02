from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class TableRepo:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.table_information_extraction_db
        self.tables = self.db.table_extraction

    def get_table_extraction_by_id(self, table_id):
        table_extraction_data = self.tables.find_one({"_id": ObjectId(table_id)})
        if table_extraction_data is not None:
            table_extraction_data = json.loads(json_util.dumps(table_extraction_data))
            table_extraction_data["_id"] = table_extraction_data["_id"]["$oid"]
        return table_extraction_data

    def get_table_extraction_by_hash_code(self, hash_code):
        table_extraction_data = self.tables.find_one({"hash_code": hash_code})
        return table_extraction_data

    def get_all_tables_extractions(self):
        cursor = self.tables.find({})
        tables_extraction_data = list(cursor)
        tables_extraction_data = json.loads(json_util.dumps(tables_extraction_data))
        for item in tables_extraction_data:
            item["_id"] = item["_id"]["$oid"]
        return tables_extraction_data

    def save_table_extraction(self, table_extraction_data):
        persisted_data = self.tables.insert_one(table_extraction_data)
        new_id = json.loads(json_util.dumps(persisted_data.inserted_id))
        return list(new_id.values())[0]

    def update_table_extraction(self, table_extraction_data):
        table_id = table_extraction_data["_id"]
        del table_extraction_data["_id"]
        result = self.tables.update_one(
            filter={"_id": ObjectId(table_id)}, update={"$set": table_extraction_data}
        )
        return result.modified_count

    def delete_table_extraction(self, table_id):
        result = self.tables.delete_one({"_id": ObjectId(table_id)})
        return result.deleted_count


# repo = TableRepo()
# with open("../../output/json/2_table2.json", "r") as file:
#     # Memuat konten file JSON
#     data = json.load(file)

# table2 = {
#     "hash_code": "80dcaf54f5b46e0e1a7d378e2a59cbb4",
#     "jenis_dokumen": "surat_kebutuhan_alat",
#     "data_ekstraksi": data,
# }

# id = repo.save(table2)
# print(id)
