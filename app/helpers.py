import os
import sys
import pandas as pd
import numpy as np
import json

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

from config import ALLOWED_EXTENSIONS

class TableArgs:
    def __init__(self, image_dir): 
        self.det_model_dir="F:/Programming/Python/Flask/TIE/PaddleOCR/ppstructure/inference/ch_PP-OCRv3_det_infer"
        self.rec_model_dir="F:/Programming/Python/Flask/TIE/PaddleOCR/ppstructure/inference/ch_PP-OCRv3_rec_infer"
        self.table_model_dir="F:/Programming/Python/Flask/TIE/PaddleOCR/ppstructure/inference/ch_ppstructure_mobile_v2.0_SLANet_infer"
        self.rec_char_dict_path= "F:/Programming/Python/Flask/TIE/PaddleOCR/ppocr/utils/ppocr_keys_v1.txt"
        self.table_char_dict_path="F:/Programming/Python/Flask/TIE/PaddleOCR/ppocr/utils/dict/table_structure_dict_ch.txt"
        self.image_dir=image_dir
        self.output="F:/Programming/Python/Flask/TIE/output"
        self.process_id = 0
        self.total_process_num = 1

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

def data_transform(dokument_type, excel_path):
    
    
    return


def surat_penyerahan_barang(excel_path):    
    header = ['No', 'Nama Materil', 'Jumlah', 'Satuan', 'Keterangan'] #set header
    df = pd.read_excel(excel_path, header=None, skiprows=4, names=header, usecols=[0, 1, 2, 4, 5]) #read excel file
    df['No'] = df['No'].fillna(0).astype(int) #change NaN to 0
    df['Jumlah'] = df['Jumlah'].fillna(0).astype(int) #change NaN to 0
    list_row_item = np.where(df['Nama Materil'].isna()) #look for coordinates that become boundaries between items
    
    # create new DataFrame for each item
    items_table = []
    start = 0
    for end in list_row_item[0]:
        item = df.iloc[start:end, :4].reset_index(drop=True)
        items_table.append(item)
        start = end + 1
    
    #Adds the last item   
    last_item = df.iloc[start:, :4]
    items_table.append(last_item)
    
    json_all_item = []
    
    #transform data for each item to json
    for i, item in enumerate(items_table):
        #divide item data into nama materill, seri, and kelengkapan
        array_row_element = np.where(item['Nama Materil'].str.contains(':'))
        
        #transform for data nama materill
        if len(array_row_element[0]) == 0 :
          bound = len(item)
        else :
          bound = array_row_element[0][0]
          
        item_nama_materil = item.iloc[0:bound,:]
        json_materil = item_nama_materil.to_json(orient='records')
        json_item = json.loads(json_materil) #change json_materil(string) to Python object (dict)
        
        
        # check if there are seri data
        if len(array_row_element[0]) >=1 :
            item_seri = item.iloc[array_row_element[0][0]:array_row_element[0][1], 1:2]
            #transform for data seri
            seri_str = ""
            for data in item_seri['Nama Materil']:
                seri_str += data
            index = seri_str.find(":")
            seri_str = seri_str[index+1:]
            seri_list = seri_str.split(",")
            json_item[0]["Seri"] = seri_list
        
        # check if there are kelengkapan data    
        if len(array_row_element[0]) >=2 :
            item_kelengkapan = item.iloc[array_row_element[0][1]+1:, 1:]
            #transform for data kelengkapan
            json_kelengkapan = item_kelengkapan.to_json(orient='records')
            json_item[0]["Kelengkapan"] = json.loads(json_kelengkapan)
        
        #add json_item to json_all_item
        json_all_item.append(json_item[0])

    return json_all_item

def surat_penerimaan_materil():
    return 

def surat_kebutuhan_alat():
    return 


json_surat1 = surat_penyerahan_barang("F:/Programming/Python/Flask/TIE/output/table/[0, 0, 1133, 907]_0.xlsx")

with open("F:/Programming/Python/Flask/TIE/output/table/data.json", "w") as file:
    json.dump(json_surat1, file)