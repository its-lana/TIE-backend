# 1. save structure_res :
# proses : konvert dari html ke excel, dan nyimpen file excelnya
# input : result tsr/recognition result dlm bntuk kode html
# output : file .txt, excel path,
# result isinya apa?
"""
result = [
'type': table/figure,
'bbox' : batas wilayah yg menjadi tabel dari gambar input, 
'img' : image nya, ngg tau yg ada bb nya atau ngga, 
'res' : koordinat cell hasil tsr, dan ada juga html nya
'img_idx': 0]
def save_structure_res(result, save_folder, img_name, img_idx=0):
    create_dir(excel_save_folder)
    copyResult(result)
    sambilWriteResKeFileTxt:
        for region in result : (cuma ada satu region, karena di gambar nya cuma ada table doang)
            potong bagian 'img'
            write isi region ke .txt 
            if tabel and res > 0 and ada html di res:
                convert_to_excel(excel_path)
                return excel_path
                
convert_to_excel :                
Mengambil representasi string dari dokumen html dan menulis satu lembar untuk setiap tabel dalam dokumen. Buku kerja ditulis ke file yang disebut filename
"""

"""
2. StructureSystem
# proses : tsr(det), ocr (det, rec), tr ke html
# input : img
# output : result(koordinat cell, html)

ada :
init :
if args.table:
    self.table_system = TableSystem(args)

call :
if self.mode == "structure":
    img = img.copy()
    

ngapain aja di sana?
"""

"""
3. TableSystem

(distance(gt_box, pred_box), 1. - compute_iou(gt_box, pred_box))
(res_distance, hasil)


brrti get_pred_html itu parameternya :
1. prediksi struktur html dari tsr
2. 

model rec :
SVTR_LCNet is a lightweight text recognition network fused by Transformer-based network [SVTR](https://arxiv.org/abs/2205.00159) and lightweight CNN-based network [PP-LCNet](https://arxiv.org/abs/2109.15099). The prediction speed of SVTR_LCNet is 20% faster than that of PP-OCRv2 recognizer while the effect is slightly worse because the distillation strategy is not adopted. In addition, the height of the input image is further increased from 32 to 48, which makes the prediction speed slightly slower, but the model effect greatly improved. The recognition accuracy reaches 73.98% (+2.08%), which is close to the accuracy of PP-OCRv2 recognizer trained with the distillation strategy.
PP-OCRv3 is further upgraded on the basis of PP-OCRv2. The overall framework of PP-OCRv3 is same as that of PP-OCRv2. The text detection model and text recognition model are further optimized, respectively. Specifically, the detection network is still optimized based on DBNet, and base model of recognition network is replaced from CRNN to [SVTR](https://arxiv.org/abs/2205.00159), which is recorded in IJCAI 2022. The block diagram of the PP-OCRv3 system is as follows (strategies in the pink box are newly introduced in PP-OCRv3):
"""
