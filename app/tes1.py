# # StructureSystem : __call__
# if self.mode == "structure":
#     ori_im = img.copy()
#     h, w = ori_im.shape[:2]
#     layout_res = [dict(bbox=None, label="table")]
#     res_list = []
#     for region in layout_res:
#         res = ""
#         x1, y1, x2, y2 = 0, 0, w, h
#         roi_img = ori_im
#         if region["label"] == "table":
#             if self.table_system is not None:
#                 res, table_time_dict = self.table_system(
#                     roi_img, return_ocr_result_in_table
#                 )
#                 time_dict["table"] += table_time_dict["table"]
#                 time_dict["table_match"] += table_time_dict["match"]
#                 time_dict["det"] += table_time_dict["det"]
#                 time_dict["rec"] += table_time_dict["rec"]

#         res_list.append(
#             {
#                 "type": region["label"].lower(),
#                 "bbox": [x1, y1, x2, y2],
#                 "img": roi_img,
#                 "res": res,
#                 "img_idx": img_idx,
#             }
#         )
#     end = time.time()
#     time_dict["all"] = end - start
#     return res_list, time_dict
