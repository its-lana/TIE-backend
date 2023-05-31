import os
import sys
import shutil


__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..\PaddleOCR")))


from flask import request, jsonify, flash, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from helpers import (
    allowed_file,
    extract_table,
    data_transform,
    get_hash_code,
    is_unique,
)
from PaddleOCR.ppstructure import table

from repository import tableRepo

repo = tableRepo.TableRepo()


# pr :  cek setiap metode yg di panggil transform_data;
@app.route("/table", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return jsonify({"error": "No file part!"}), 400
        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return jsonify({"error": "No selected file!"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            document_type = request.form.get("document_type")

            img_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(img_path)
            hash_code = get_hash_code(img_path=img_path)
            # Has the image been extracted?
            if not is_unique(hash_code):
                return jsonify({"error": "Image has been extracted!"}), 400

            excel_path = extract_table(img_path)
            extraction_data = data_transform(document_type, excel_path, hash_code)
            os.remove(img_path)
            shutil.rmtree(os.path.dirname(os.path.abspath(excel_path)))

            json_data = {}
            json_data["hash_code"] = hash_code
            json_data["jenis_dokumen"] = document_type.replace("_", " ").title()
            json_data["data_ekstraksi"] = extraction_data

            data_id = repo.save(json_data)
            response = jsonify(repo.get_document_by_id(data_id))
            response.status_code = 200

            return response
            # return redirect(url_for("extract_table", file_path=img_path))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <select name="document_type">
            <option value="surat_penyerahan_barang">Surat Penyerahan Barang</option>
            <option value="surat_penerimaan_materil">Surat Penerimaan Materil</option>
            <option value="surat_kebutuhan_alat">Surat Kebutuhan Alat</option>
        </select>
      <input type=submit value=Upload>
    </form>
    """


@app.route("/table/uploads/<name>")
def download_file(name):
    return send_from_directory("..\img", name)


# @app.route("/table/extract/<name>")
# def extract_table(name):
#     args = TableArgs(
#         image_dir="F:/Programming/Python/Flask/TIE/PaddleOCR/ppstructure/table/table3.jpg"
#     )
#     table.predict_table.main(args=args)
#     return send_from_directory("..\img", name)


########################################################### new


# @app.route("/table", methods=["GET"])
# def get_all_data_extraction():
#     data_extractions = repo.get_all()
#     response = jsonify(data_extractions)
#     response.status_code = 200
#     return response


@app.route("/table/<string:img_hash_code>", methods=["GET"])
def get_data_extraction(img_hash_code):
    data_extraction = repo.get_document_by_id(img_hash_code)
    response = jsonify(data_extraction)
    response.status_code = 200
    return response


@app.route("/table/<string:img_hash_code>", methods=["PUT"])
def update_data_extraction(img_hash_code):
    body = request.get_json()
    updated = repo.update(body)

    if updated >= 1:
        response = jsonify(repo.get_document_by_id(img_hash_code))
        response.status_code = 200
    else:
        response = jsonify({"status_code": 404})
    return response


@app.route("/table/<string:img_hash_code>", methods=["DELETE"])
def delete_data_extraction(img_hash_code):
    deleted = repo.delete(img_hash_code)

    if deleted >= 1:
        response = jsonify({"status_code": 200})
    else:
        response = jsonify({"status_code": 404})
    return response
