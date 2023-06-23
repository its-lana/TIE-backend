import os
import sys
import shutil
import bson


__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..\PaddleOCR")))


from flask import (
    request,
    jsonify,
    flash,
    redirect,
    url_for,
    send_from_directory,
    make_response,
)

from app import app
from werkzeug.utils import secure_filename
from helpers import (
    extract_table,
    data_transform,
    get_hash_code,
    is_unique,
    files_handling,
    images_stitching_1,
    images_stitching_2,
    extract_html,
    html_transform,
)
from PaddleOCR.ppstructure import table

from repository import tableRepo, htmlRepo, documentTypeRepo

table_repo = tableRepo.TableRepo()
html_repo = htmlRepo.HtmlRepo()
doc_type_repo = documentTypeRepo.DocumentTypeRepo()


@app.route("/html", methods=["POST"])
def get_html():
    files = []
    files_react = request.files
    for file_key in files_react:
        files.append(files_react[file_key])
    img_path_list = files_handling(files)
    if len(img_path_list) == 0:
        return jsonify({"error": "Selected files are not allowed!"}), 400
    elif len(img_path_list) == 1:
        img_path = img_path_list[0]
    else:
        img_path = images_stitching_1(img_path_list)
    html_path = extract_html(img_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Mengatur konten respons sebagai string HTML
    response = make_response(html_content)
    response.headers["Content-Type"] = "text/html"

    # Menghapus file show.html (opsional)
    # os.remove(os.path.join(output_dir, 'show.html'))

    # Mengembalikan respons API dengan data HTML sebagai string
    return response


@app.route("/html/transform", methods=["POST"])
def html_transform_to_json():
    html_data = request.json.get("htmlData")
    json_data = html_transform(html_data)
    data_id = html_repo.save_html_extraction(json_data)
    response = jsonify(html_repo.get_table_extraction_by_id(data_id))
    response.status_code = 200

    return response


@app.route("/table", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        document_type = request.form.get("document_type")
        print(document_type)
        if document_type is None:
            return jsonify({"error": "No selected document type!"}), 400
        files = []
        files_react = request.files
        for file_key in files_react:
            files.append(files_react[file_key])
            print(1)
        print(type(files))
        print(len(files))

        if len(files) == 0:
            return jsonify({"error": "No selected file!"}), 400

        # get path image list from files request
        img_path_list = files_handling(files)
        if len(img_path_list) == 0:
            return jsonify({"error": "Selected files are not allowed!"}), 400
        elif len(img_path_list) == 1:
            img_path = img_path_list[0]
        else:
            img_path = images_stitching_1(img_path_list)
        print("di atas hashcode")
        hash_code = get_hash_code(img_path)
        # Has the image been extracted?
        if not is_unique(hash_code):
            return jsonify({"error": "Image has been extracted!"}), 400

        # document_type = request.form.get("document_type")
        print(document_type)
        excel_path = extract_table(img_path)
        # os.remove(img_path)
        print(excel_path)
        extraction_data = data_transform(document_type, excel_path, hash_code)
        shutil.rmtree(os.path.dirname(os.path.abspath(excel_path)))

        json_data = {}
        json_data["hash_code"] = hash_code
        json_data["jenis_dokumen"] = document_type.replace("_", " ").title()
        json_data["data_ekstraksi"] = extraction_data

        data_id = table_repo.save_table_extraction(json_data)
        response = jsonify(table_repo.get_table_extraction_by_id(data_id))
        response.status_code = 200

        return response
        # return redirect(url_for("extract_table", file_path=img_path))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file multiple>
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


@app.route("/table/all", methods=["GET"])
def get_all_data_extraction():
    data_extractions = table_repo.get_all_tables_extractions()
    response = jsonify(data_extractions)
    response.status_code = 200
    return response


@app.route("/table/<string:table_id>", methods=["GET"])
def get_data_extraction(table_id):
    data_extraction = table_repo.get_table_extraction_by_id(table_id)
    response = jsonify(data_extraction)
    response.status_code = 200
    print(data_extraction)
    print("====")
    print(jsonify(data_extraction))
    return response


@app.route("/table/<string:table_id>", methods=["PUT"])
def update_data_extraction(table_id):
    extraction_data = request.get_json()

    # check there are data with that id
    table_data = table_repo.get_table_extraction_by_id(table_id)
    if table_data is None:
        return jsonify({"error": "No data with that id!"}), 400

    # dapetin jenis dokumen dari table_data
    document_type = table_data["jenis_dokumen"]
    # get data jenis dokumen by nama dokumen
    document_type_data = doc_type_repo.get_doc_type_by_name(document_type)
    # dapetin daftar kolom dari data jenis dokumen
    column_list = document_type_data["daftar_kolom"]

    # get list column with tipe_data int
    int_column_list = [
        column["nama_kolom"] for column in column_list if column["tipe_data"] == "int"
    ]
    # convert to int
    for data in extraction_data:
        for column in int_column_list:
            if type(data[column]) == str:
                if data[column].isnumeric() == False:
                    data[column] = data[column].replace(".", "")
                    data[column] = data[column].replace(",", "")
                    if data[column].isnumeric() == False:
                        data[column] = 0
            data[column] = bson.Int64(int(data[column]))

    # update data
    updated = table_repo.update_table_extraction(table_id, extraction_data)

    response = jsonify(table_repo.get_table_extraction_by_id(table_id))
    response.status_code = 200
    return response


@app.route("/table/<string:table_id>", methods=["DELETE"])
def delete_data_extraction(table_id):
    deleted = table_repo.delete_table_extraction(table_id)

    if deleted >= 1:
        response = jsonify({"status_code": 200})
    else:
        response = jsonify({"status_code": 404})
    return response
