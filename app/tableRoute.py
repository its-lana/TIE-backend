import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..\PaddleOCR")))


from flask import request, jsonify, flash, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from helpers import allowed_file, extract_table, data_transform
from PaddleOCR.ppstructure import table

from repository import tableRepo

repo = tableRepo.TableRepo()


@app.route("/table", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("extract_table", name=filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
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


@app.route("/table", methods=["GET"])
def get_all_data_extraction():
    data_extractions = repo.get_all()
    response = jsonify(data_extractions)
    response.status_code = 200
    return response


@app.route("/table", methods=["POST"])
def extract_table():
    data = request.get_data()
    image = data.img_path
    dokument_type = data.dokument_type
    # tambahin pengecekan hashcode img
    excel_path = extract_table(image)
    json_data = data_transform(dokument_type, excel_path)
    new_data = repo.save(json_data)
    response = jsonify(repo.get_id(new_data))
    response.status_code = 200
    return response


@app.route("/table/<string:img_hash_code>", methods=["GET"])
def get_data_extraction(img_hash_code):
    data_extraction = repo.get_id(img_hash_code)
    response = jsonify(data_extraction)
    response.status_code = 200
    return response


@app.route("/table/<string:img_hash_code>", methods=["PUT"])
def update_data_extraction(img_hash_code):
    body = request.get_json()
    updated = repo.update(body)

    if updated >= 1:
        response = jsonify(repo.get_id(img_hash_code))
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
