import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..\PaddleOCR')))

# print(sys.path)
# from helpers import TableArgs

# args = TableArgs(image_dir="../../img/table.jpg")
# print (args.image_dir)
# print (type(args.image_dir))

import cv2
from PaddleOCR import PPStructure,save_structure_res

table_engine = PPStructure(layout=False, show_log=True)

save_folder = '../output'
img_path = '../img/2_table2.jpg'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

# for line in result:
#     line.pop('img')
#     print(line)