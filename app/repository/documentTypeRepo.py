from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class DocumentTypeRepo:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.table_information_extraction_db
        self.doc_types = self.db.document_types

    def get_doc_type_by_id(self, doc_type_id):
        doc_type_data = self.doc_types.find_one({"_id": ObjectId(doc_type_id)})
        if doc_type_data is not None:
            doc_type_data = json.loads(json_util.dumps(doc_type_data))
            doc_type_data["_id"] = doc_type_data["_id"]["$oid"]
        return doc_type_data

    def get_all_doc_types(self):
        cursor = self.doc_types.find({})
        doc_types_data = list(cursor)
        doc_types_data = json.loads(json_util.dumps(doc_types_data))
        for item in doc_types_data:
            item["_id"] = item["_id"]["$oid"]
        return doc_types_data

    def save_doc_type(self, doc_type_data):
        persisted_data = self.doc_types.insert_one(doc_type_data)
        new_id = json.loads(json_util.dumps(persisted_data.inserted_id))
        return list(new_id.values())[0]

    def update_doc_type(self, doc_type_data):
        doc_type_id = doc_type_data["_id"]
        del doc_type_data["_id"]
        result = self.doc_types.update_one(
            filter={"_id": ObjectId(doc_type_id)}, update={"$set": doc_type_data}
        )
        return result.modified_count

    def delete_doc_type(self, doc_type_id):
        result = self.doc_types.delete_one({"_id": ObjectId(doc_type_id)})
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
