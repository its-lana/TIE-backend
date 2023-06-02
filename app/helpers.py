import os
import sys
import pandas as pd
import numpy as np
import json
import cv2
import hashlib
from werkzeug.utils import secure_filename

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..\PaddleOCR")))


from config import ALLOWED_EXTENSIONS, EXTRACT_RESULT_PATH, JSON_DIR, UPLOAD_IMAGE_PATH
from PaddleOCR import PPStructure, save_structure_res
from repository import tableRepo

repo = tableRepo.TableRepo()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_hash_code(img_path):
    # Read the file in binary mode and calculate the MD5 hash
    with open(img_path, "rb") as file:
        content = file.read()
        md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash


def is_unique(hash_code):
    result = repo.get_table_extraction_by_hash_code(hash_code)
    return result is None


# return : excel file path
def extract_table(img_path):
    table_engine = PPStructure(layout=False, show_log=True)
    save_folder = EXTRACT_RESULT_PATH
    img = cv2.imread(img_path)
    result = table_engine(img)
    img_filename = os.path.basename(img_path).split(".")[0]
    excel_path = save_structure_res(result, save_folder, img_filename)

    return excel_path


def data_transform(dokument_type, excel_path, hash_code):
    json_data = []
    if dokument_type == "surat_penyerahan_barang":
        json_data = surat_penyerahan_barang(excel_path=excel_path, hash_code=hash_code)
    elif dokument_type == "surat_penerimaan_materil":
        json_data = surat_penerimaan_materil(excel_path=excel_path, hash_code=hash_code)
    elif dokument_type == "surat_kebutuhan_alat":
        json_data = surat_kebutuhan_alat(excel_path=excel_path, hash_code=hash_code)
    return json_data


def surat_penyerahan_barang(excel_path, hash_code):
    header = ["No", "Nama Materil", "Jumlah", "Satuan", "Keterangan"]  # set header
    df = pd.read_excel(
        excel_path, header=None, skiprows=4, names=header, usecols=[0, 1, 2, 4, 5]
    )  # read excel file
    df["No"] = df["No"].fillna(0).astype(int)  # change NaN to 0
    df["Jumlah"] = df["Jumlah"].fillna(0).astype(int)  # change NaN to 0
    list_row_item = np.where(
        df["Nama Materil"].isna()
    )  # look for coordinates that become boundaries between items

    # create new DataFrame for each item
    items_table = []
    start = 0
    for end in list_row_item[0]:
        item = df.iloc[start:end, :4].reset_index(drop=True)
        items_table.append(item)
        start = end + 1

    # Adds the last item
    last_item = df.iloc[start:, :4]
    items_table.append(last_item)

    json_all_items = []

    # transform data for each item to json
    for i, item in enumerate(items_table):
        # divide item data into nama materill, seri, and kelengkapan
        array_row_element = np.where(item["Nama Materil"].str.contains(":"))

        # transform for data nama materill
        if len(array_row_element[0]) == 0:
            bound = len(item)
        else:
            bound = array_row_element[0][0]

        item_nama_materil = item.iloc[0:bound, :]
        json_materil = item_nama_materil.to_json(orient="records")
        json_item = json.loads(
            json_materil
        )  # change json_materil(string) to Python object (dict)

        # check if there are seri data
        if len(array_row_element[0]) >= 1:
            item_seri = item.iloc[
                array_row_element[0][0] : array_row_element[0][1], 1:2
            ]
            # transform for data seri
            seri_str = ""
            for data in item_seri["Nama Materil"]:
                seri_str += data
            index = seri_str.find(":")
            seri_str = seri_str[index + 1 :]
            seri_list = seri_str.split(",")
            json_item[0]["Seri"] = seri_list

        # check if there are kelengkapan data
        if len(array_row_element[0]) >= 2:
            item_kelengkapan = item.iloc[array_row_element[0][1] + 1 :, 1:]
            # transform for data kelengkapan
            json_kelengkapan = item_kelengkapan.to_json(orient="records")
            json_item[0]["Kelengkapan"] = json.loads(json_kelengkapan)

        # add json_item to json_all_item
        json_all_items.append(json_item[0])

    json_filename = hash_code + ".json"
    json_path = os.path.join(JSON_DIR, json_filename)
    with open(json_path, "w") as file:
        json.dump(json_all_items, file)
    return json_all_items


def surat_penerimaan_materil(excel_path, hash_code):
    header = [
        "No Urut",
        "Nama dan Kode Materiil",
        "Satuan",
        "Banyaknya (Angka)",
        "Jumlah (Rp)",
        "Keterangan",
    ]
    df = pd.read_excel(
        excel_path, header=None, skiprows=3, names=header, usecols=[0, 1, 2, 3, 5, 6]
    )
    df["No Urut"] = range(0, len(df))

    # change NaN with 0
    df["Banyaknya (Angka)"] = df["Banyaknya (Angka)"].fillna(0)
    df["Jumlah (Rp)"] = df["Jumlah (Rp)"].fillna(0)
    # convert column data type to int
    column_to_convert = ["Banyaknya (Angka)", "Jumlah (Rp)"]
    for column_name in column_to_convert:
        convert_to_int(df, column_name)

    json_filename = hash_code + ".json"
    json_path = os.path.join(JSON_DIR, json_filename)
    json_all_items = df_to_json(df, json_path)

    return json_all_items


def surat_kebutuhan_alat(excel_path, hash_code):
    header = [
        "No",
        "Jenis Materiil",
        "Satuan",
        "Indeks OPS",
        "Kebut OPS",
        "Nyata",
        "Terdukung",
        "Kurang",
        "Keterangan",
    ]
    df = pd.read_excel(
        excel_path,
        header=None,
        skiprows=2,
        names=header,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    )
    df["No"] = range(1, len(df) + 1)

    # change NaN with 0
    df["Indeks OPS"] = df["Indeks OPS"].fillna(0)
    df["Kebut OPS"] = df["Kebut OPS"].fillna(0)
    df["Nyata"] = df["Nyata"].fillna(0)
    df["Terdukung"] = df["Terdukung"].fillna(0)
    df["Kurang"] = df["Kurang"].fillna(0)
    # convert column data type to int
    column_to_convert = ["Indeks OPS", "Kebut OPS", "Nyata", "Terdukung", "Kurang"]
    for column_name in column_to_convert:
        convert_to_int(df, column_name)

    json_filename = hash_code + ".json"
    json_path = os.path.join(JSON_DIR, json_filename)
    json_all_items = df_to_json(df, json_path)

    return json_all_items


# init state : list file
# final state : di save dan return list path img nya, tp sblm itu d cek ini itu dulu
# hashcode ngg masuk sini
def files_handling(files):
    path_img_list = []
    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(UPLOAD_IMAGE_PATH, filename)
            print(img_path)
            file.save(img_path)
            path_img_list.append(img_path)
    return path_img_list


# init state : list path img
# final state : digabung jadi satu file
def images_stitching(img_path_list):
    img_list = []
    for path in img_path_list:
        img = cv2.imread(path)
        img_list.append(img)
        os.remove(path)

    # resize the width of the image to follow the first image
    for i in range(len(img_list) - 1):
        img_list[i + 1] = cv2.resize(
            img_list[i + 1], (img_list[0].shape[1], img_list[i + 1].shape[0])
        )

    # Create a blank image with sufficient size
    width = img_list[0].shape[1]
    height = 0
    for i in range(len(img_list)):
        height += img_list[i].shape[0]
    result = np.zeros((height, width, 3), dtype=np.uint8)

    # placement of images based on sequence
    start = 0
    for img in img_list:
        end = start + img.shape[0]
        result[start:end, :] = img
        start = end
    filename = "combined_image.jpg"
    file_path = os.path.join(UPLOAD_IMAGE_PATH, filename)

    # save image to file
    cv2.imwrite(file_path, result)
    return file_path


def df_to_json(df, json_path):
    json_str = df.to_json(orient="records")  # df to json string
    json_list = json.loads(json_str)  # str to json list
    with open(json_path, "w") as file:
        json.dump(json_list, file)
    return json_list


# convert dataframe column to integer
def convert_to_int(df, column_name):
    print("Converting " + column_name + " to Int")
    for index, value in enumerate(df[column_name]):
        if type(df.at[index, column_name]) == str:
            if df.at[index, column_name].isnumeric() == False:
                df.at[index, column_name] = df.at[index, column_name].replace(".", "")
                df.at[index, column_name] = df.at[index, column_name].replace(",", "")
                if df.at[index, column_name].isnumeric() == False:
                    df.at[index, column_name] = 0
        df.at[index, column_name] = int(df.at[index, column_name])


# json_surat1 = surat_penyerahan_barang(
#     "F:/Programming/Python/Flask/TIE/output/table/[0, 0, 1133, 907]_0.xlsx"
# )

# with open("F:/Programming/Python/Flask/TIE/output/table/data.json", "w") as file:
#     json.dump(json_surat1, file)
