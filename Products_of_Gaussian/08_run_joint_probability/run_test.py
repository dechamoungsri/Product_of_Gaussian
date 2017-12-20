
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

sys.path.append('../')

from tool_box.util.utility import Utility
from tool_box.distortion.distortion_utility import Distortion

from PoG_Utility.pog_utility import PoGUtility

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import dct, idct
from numpy.linalg import inv

# vuv = np.load('/work/w21/decha/Interspeech_2017/GPR_data/450/predictive_distribution_align/vuv/predictive_distribution/tscsdj01/class.npy')

# print set(vuv)
# print len(vuv[vuv==-1]), len(vuv[vuv==1])

# lf0 = np.load('/work/w21/decha/Interspeech_2017/GPR_data/450/param_align/lf0/param_mean/tscsdj01.npy')

# print len(lf0[lf0<0])

# arr = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16], [17,18,19,20]])
# arr = np.delete(arr, [0,2], 1)
# print arr

arr = np.array([[0,1,2,3,4,5,6], [0,1,2,3,4,5,6]])
arr[1] = -1

print arr
