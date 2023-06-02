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
