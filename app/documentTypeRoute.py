import os
import sys
from flask import request, jsonify


__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))

from app import app
from repository import documentTypeRepo
from helpers import files_handling, extract_table, header_handler

repo = documentTypeRepo.DocumentTypeRepo()


@app.route("/document-types/extract-header", methods=["POST"])
def extract_header():
    files = []
    files_react = request.files
    for file_key in files_react:
        files.append(files_react[file_key])
    img_path_list = files_handling(files)
    img_path = img_path_list[0]
    excel_path = extract_table(img_path)
    json_data = header_handler(excel_path)
    response = jsonify(json_data)
    response.status_code = 200
    return response


@app.route("/document-types", methods=["POST"])
def add_document_types():
    body = request.get_json()
    print(body)
    document_name = body["nama_dokumen"]
    if repo.get_doc_type_by_name(document_name) is not None:
        return jsonify({"error": "Document name already exist!"}), 400
    doc_type_id = repo.save_doc_type(body)
    response = jsonify(repo.get_doc_type_by_id(doc_type_id))
    response.status_code = 200
    return response


@app.route("/document-types/all", methods=["GET"])
def get_all_document_types():
    document_types = repo.get_all_doc_types()
    response = jsonify(document_types)
    response.status_code = 200
    return response


@app.route("/document-types/<string:document_type_id>", methods=["GET"])
def get_document_type(document_type_id):
    document_type = repo.get_doc_type_by_id(document_type_id)
    response = jsonify(document_type)
    response.status_code = 200
    return response


# note : data yg dikiri fe pas put, harus ada id nya,
@app.route("/document-types/<string:document_type_id>", methods=["PUT"])
def update_document_type(document_type_id):
    body = request.get_json()
    updated = repo.update_doc_type(body)

    if updated >= 1:
        response = jsonify(repo.get_doc_type_by_id(document_type_id))
        response.status_code = 200
    else:
        response = jsonify({"status_code": 404})
    return response


@app.route("/document-types/<string:document_type_id>", methods=["DELETE"])
def delete_document_type(document_type_id):
    deleted = repo.delete_doc_type(document_type_id)

    if deleted >= 1:
        response = jsonify({"status_code": 200})
    else:
        response = jsonify({"status_code": 404})
    return response
