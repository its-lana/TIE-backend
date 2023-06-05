# import paddle
# paddle.utils.run_check()

# import tensorflow as tf

# # Check if GPU is available and if CuDNN is enabled
# if tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None):
#   print("GPU is available")
#   print("CuDNN is enabled:", tf.test.is_built_with_cudnn())
# else:
#   print("GPU is not available")
# import os
import sys, os

# __dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append("F:\Programming\Python\Flask\TIE")
sys.path.append("F:\Programming\Python\Flask\TIE\\tes")

# import tes

# tes.tesla.lala()
from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class TemplateRepo:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.table_information_extraction_db
        self.templates = self.db.document_type_templates

    def save(self, template_data):
        persisted_data = self.templates.insert_one(template_data)
        new_id = json.loads(json_util.dumps(persisted_data.inserted_id))
        return list(new_id.values())[0]


template2 = {
    "nama_dokumen": "Surat Penerimaan Materil",
    "jenis_tabel": "Umum",
    "daftar_kolom": [
        {"nama_kolom": "No Urut", "tipe_data": "int"},
        {"nama_kolom": "Nama dan Kode Materiil", "tipe_data": "string"},
        {"nama_kolom": "Satuan", "tipe_data": "string"},
        {"nama_kolom": "Banyaknya (Angka)", "tipe_data": "int"},
        {"nama_kolom": "Banyaknya (Huruf)", "tipe_data": "string"},
        {"nama_kolom": "Harga (Jumlah (Rp))", "tipe_data": "int"},
        {"nama_kolom": "Ket", "tipe_data": "string"},
    ],
}

template3 = {
    "nama_dokumen": "Surat Kebutuhan Alat",
    "jenis_tabel": "Umum",
    "daftar_kolom": [
        {"nama_kolom": "NO", "tipe_data": "int"},
        {"nama_kolom": "JENIS MATERIIL", "tipe_data": "string"},
        {"nama_kolom": "SAT", "tipe_data": "string"},
        {"nama_kolom": "INDEKS OPS", "tipe_data": "int"},
        {"nama_kolom": "KEBUT OPS", "tipe_data": "int"},
        {"nama_kolom": "NYATA", "tipe_data": "int"},
        {"nama_kolom": "TERDUKUNG", "tipe_data": "int"},
        {"nama_kolom": "KURANG", "tipe_data": "int"},
        {"nama_kolom": "KET", "tipe_data": "string"},
    ],
}

repo = TemplateRepo()
id_template2 = repo.save(template2)
id_template3 = repo.save(template3)


def common_table(column_list, excel_path, hash_code):
    # get list column list
    column_name_list = [column["nama_kolom"] for column in column_list]
    # generate use cols: generate list 0..len(column name list)
    use_cols = list(range(len(column_name_list)))
    # read excel
    df = pd.read_excel(
        excel_path, header=None, names=column_name_list, usecols=use_cols
    )
    # skiprows
    df[column_name_list[1]] = df[column_name_list[1]].fillna("")
    skiprows = df[df[column_name_list[1]].str.contains("2")].index.tolist()[0] + 1
    df = df.iloc[skiprows:]
    df = df.reset_index(drop=True)
    # replace "No" column value with generate number
    df[column_name_list[0]] = range(1, len(df) + 1)

    # get list column with tipe_data int
    int_column_list = [
        column["nama_kolom"] for column in column_list if column["tipe_data"] == "int"
    ]
    int_column_list = int_column_list[1:]
    # change NaN in int_column_list with 0 and convert to int
    for column_name in int_column_list:
        df[column_name] = df[column_name].fillna(0)
        convert_to_int(df, column_name)

    # transform to json
    json_filename = hash_code + ".json"
    json_path = os.path.join(JSON_DIR, json_filename)
    json_all_items = df_to_json(df, json_path)

    return json_all_items
