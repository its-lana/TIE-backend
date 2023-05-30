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
img_path = "F:\Programming\Python\Flask\TIE\img\z_table2.jpg"
print(os.path.basename(img_path).split(".")[0])
