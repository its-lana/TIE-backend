from pymongo import MongoClient
from bson import json_util, ObjectId
from collections import OrderedDict
import json

client = MongoClient("mongodb://localhost:27017")
db = client["table_information_extraction_db"]

doc_types = db["table_extraction"]


def get_all_doc_types():
    cursor = doc_types.find({})
    doc_types_data = list(cursor)
    doc_types_data = json.loads(json_util.dumps(doc_types_data))
    for item in doc_types_data:
        item["_id"] = item["_id"]["$oid"]
    return doc_types_data


def get_doc_type_by_name(doc_type_name):
    doc_type_data = doc_types.find_one({"jenis_dokumen": doc_type_name})
    if doc_type_data is not None:
        doc_type_data = json.loads(json_util.dumps(doc_type_data))
        doc_type_data["_id"] = doc_type_data["_id"]["$oid"]
    return doc_type_data


json_data = get_doc_type_by_name("Surat Kebutuhan Alat")
print(json_data["data_ekstraksi"][0])
